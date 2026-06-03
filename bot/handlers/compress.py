"""Хэндлер сжатия видео и фотографий — FSM.

Флоу:
  1. waiting_file   — юзер шлёт видео/фото/документ
  2. waiting_preset — юзер выбирает пресет low/medium/high
  3. processing     — обработка ffmpeg/Pillow, отправка результата, cleanup

Cleanup tmp_dir — синхронно в try/finally. Local Bot API сам файлы не чистит.
"""
from __future__ import annotations

import asyncio
import logging
import os
import shutil
import tempfile
from pathlib import Path

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message

from bot.config import settings
from bot.database import async_session
from bot.database.crud import (
    get_user_language,
    increment_user_compress_count,
)
from bot.emojis import E
from bot.i18n import t
from bot.keyboards.inline import (
    get_back_keyboard,
    get_compress_cancel_keyboard,
    get_compress_preset_keyboard,
    get_start_keyboard,
)
from bot.services.compressor import (
    CompressorError,
    classify_error,
    compress_photo,
    compress_video,
    get_media_info,
)
from bot.utils.fsm_cleanup import cleanup_state

logger = logging.getLogger(__name__)
router = Router()

TMP_ROOT = "/tmp/compress_bot"

# Local Bot API принимает до 2 ГБ
MAX_INPUT_SIZE = 2 * 1024 * 1024 * 1024
# результат не должен превышать 1.9 ГБ — выше Telegram режет даже с Local API
MAX_OUTPUT_SIZE = int(1.9 * 1024 * 1024 * 1024)


class CompressStates(StatesGroup):
    waiting_file = State()
    waiting_preset = State()
    processing = State()


# защита от двойного клика на пресет
_user_locks: dict[int, asyncio.Lock] = {}


def _get_user_lock(user_id: int) -> asyncio.Lock:
    lock = _user_locks.get(user_id)
    if lock is None:
        lock = asyncio.Lock()
        _user_locks[user_id] = lock
    return lock


# ---------- утилиты ----------

def _fmt_size(num_bytes: int | float | None) -> str:
    if not num_bytes:
        return "?"
    n = float(num_bytes)
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if n < 1024 or unit == "ГБ":
            return f"{n:.1f} {unit}" if unit != "Б" else f"{int(n)} {unit}"
        n /= 1024
    return f"{n:.1f} ГБ"


def _fmt_duration(seconds: float) -> str:
    s = int(round(seconds))
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h:d}:{m:02d}:{sec:02d}"
    return f"{m:d}:{sec:02d}"


async def _get_lang(user_id: int) -> str:
    async with async_session() as session:
        return await get_user_language(session, user_id)


def _detect_media_kind(message: Message) -> tuple[str | None, str | None, int, str]:
    """Определяет тип медиа и возвращает (kind, file_id, file_size, file_name_hint).

    kind ∈ {"video", "photo", None}. None — формат не подходит.
    """
    # видео
    if message.video is not None:
        v = message.video
        return (
            "video",
            v.file_id,
            v.file_size or 0,
            v.file_name or f"video_{v.file_unique_id}.mp4",
        )
    if message.animation is not None:
        a = message.animation
        return (
            "video",
            a.file_id,
            a.file_size or 0,
            a.file_name or f"animation_{a.file_unique_id}.mp4",
        )
    # photo — массив, берём наибольшее
    if message.photo:
        ph = message.photo[-1]
        return (
            "photo",
            ph.file_id,
            ph.file_size or 0,
            f"photo_{ph.file_unique_id}.jpg",
        )
    # document — смотрим mime
    if message.document is not None:
        d = message.document
        mime = (d.mime_type or "").lower()
        if mime.startswith("video/"):
            return ("video", d.file_id, d.file_size or 0,
                    d.file_name or f"video_{d.file_unique_id}.mp4")
        if mime.startswith("image/") or mime in ("image/heic", "image/heif"):
            ext = ".jpg"
            if d.file_name and "." in d.file_name:
                ext = "." + d.file_name.rsplit(".", 1)[-1]
            return ("photo", d.file_id, d.file_size or 0,
                    d.file_name or f"photo_{d.file_unique_id}{ext}")
    return (None, None, 0, "")


# ---------- приём файла ----------

@router.message(F.video | F.photo | F.animation | F.document)
async def handle_file(message: Message, state: FSMContext) -> None:
    """Принимает видео/фото/документ, скачивает в tmp_dir, переходит к выбору пресета."""
    current = await state.get_state()
    lang = await _get_lang(message.from_user.id)

    # во время обработки новый файл не принимаем
    if current == CompressStates.processing.state:
        await message.answer(t("compress.busy", lang), parse_mode="HTML")
        return

    kind, file_id, file_size, file_name_hint = _detect_media_kind(message)
    if not kind or not file_id:
        # документ "не-медиа" или непонятный тип — отвечаем только если мы в waiting_file
        if current == CompressStates.waiting_file.state:
            await message.answer(
                t("compress.error_not_media", lang),
                reply_markup=get_compress_cancel_keyboard(lang),
                parse_mode="HTML",
            )
        return

    # ПРОВЕРКА РАЗМЕРА ДО любого cleanup — чтобы большой файл не сбросил активную сессию
    if file_size and file_size > MAX_INPUT_SIZE:
        await message.answer(t("compress.error_too_big", lang), parse_mode="HTML")
        return

    # если в FSM уже есть прошлая сессия (waiting_preset) — чистим её
    if current == CompressStates.waiting_preset.state:
        await cleanup_state(state)

    os.makedirs(TMP_ROOT, exist_ok=True)
    tmp_dir = tempfile.mkdtemp(prefix="compress_", dir=TMP_ROOT)

    safe_name = Path(file_name_hint).name or ("input.mp4" if kind == "video" else "input.jpg")
    input_path = str(Path(tmp_dir) / safe_name)

    status_msg = await message.answer(
        t("compress.downloading", lang), parse_mode="HTML",
    )

    # ---------- скачивание ----------
    api_file_path: str | None = None
    try:
        file_obj = await message.bot.get_file(file_id)
        api_file_path = file_obj.file_path  # type: ignore[assignment]

        if api_file_path and api_file_path.startswith("/"):
            # Local Bot API — файл лежит локально
            shutil.move(api_file_path, input_path)
        else:
            await message.bot.download_file(api_file_path, destination=input_path)
    except Exception as exc:
        logger.exception("download: не удалось получить file_id=%s: %s", file_id, exc)
        # Local Bot API сам файлы не чистит — если shutil.move упал, файл остался в bot-api-data
        if api_file_path and api_file_path.startswith("/"):
            try:
                Path(api_file_path).unlink(missing_ok=True)
            except OSError:
                pass
        shutil.rmtree(tmp_dir, ignore_errors=True)
        try:
            await status_msg.edit_text(
                t("compress.error_download", lang), parse_mode="HTML",
            )
        except Exception:
            await message.answer(t("compress.error_download", lang), parse_mode="HTML")
        return

    # ---------- probe ----------
    # kind берём из MIME-сообщения (см. _detect_media_kind) и доверяем ему:
    # ffprobe видит JPEG как видеопоток mjpeg и угадывание ломается.
    try:
        info = await get_media_info(Path(input_path), kind=kind)
    except CompressorError as exc:
        logger.warning("probe: %s", exc)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        try:
            await status_msg.edit_text(
                t("compress.error_unsupported", lang), parse_mode="HTML",
            )
        except Exception:
            await message.answer(t("compress.error_unsupported", lang), parse_mode="HTML")
        return

    real_kind = kind

    size = file_size or os.path.getsize(input_path)

    await state.set_state(CompressStates.waiting_preset)
    await state.update_data(
        tmp_dir=tmp_dir,
        input_path=input_path,
        media_type=real_kind,
        file_size=size,
    )

    if real_kind == "video":
        text = t(
            "compress.file_received_video", lang,
            duration=_fmt_duration(float(info.get("duration") or 0)),
            size=_fmt_size(size),
            width=info.get("width") or "?",
            height=info.get("height") or "?",
        )
    else:
        text = t(
            "compress.file_received_photo", lang,
            size=_fmt_size(size),
            width=info.get("width") or "?",
            height=info.get("height") or "?",
        )

    try:
        await status_msg.edit_text(
            text,
            reply_markup=get_compress_preset_keyboard(lang),
            parse_mode="HTML",
        )
    except Exception:
        await message.answer(
            text,
            reply_markup=get_compress_preset_keyboard(lang),
            parse_mode="HTML",
        )


# ---------- выбор пресета и обработка ----------

@router.callback_query(
    CompressStates.waiting_preset, F.data.startswith("compress_preset:"),
)
async def handle_preset(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await _get_lang(callback.from_user.id)
    preset = callback.data.split(":", 1)[1]
    if preset not in ("low", "medium", "high"):
        await callback.answer()
        return

    # защита от двойного клика — опираемся на проверку state внутри async with lock
    lock = _get_user_lock(callback.from_user.id)

    async with lock:
        current = await state.get_state()
        if current != CompressStates.waiting_preset.state:
            await callback.answer()
            return

        data = await state.get_data()
        tmp_dir = data.get("tmp_dir")
        input_path = data.get("input_path")
        media_type = data.get("media_type")

        if (
            not tmp_dir
            or not input_path
            or not media_type
            or not os.path.exists(input_path)
        ):
            await cleanup_state(state)
            try:
                await callback.message.edit_text(
                    t("compress.error_download", lang),
                    reply_markup=get_back_keyboard(lang),
                    parse_mode="HTML",
                )
            except Exception:
                pass
            await callback.answer()
            return

        # переводим в processing ДО любых await — второй клик не пройдёт
        await state.set_state(CompressStates.processing)
        await callback.answer()
        try:
            await callback.message.edit_text(
                t("compress.processing", lang), parse_mode="HTML",
            )
        except Exception:
            pass

        # выходное имя
        if media_type == "video":
            output_path = str(Path(tmp_dir) / f"out_{preset}.mp4")
        else:
            output_path = str(Path(tmp_dir) / f"out_{preset}.jpg")

        try:
            if media_type == "video":
                result = await compress_video(
                    input_path=Path(input_path),
                    output_path=Path(output_path),
                    preset=preset,
                )
            else:
                result = await compress_photo(
                    input_path=Path(input_path),
                    output_path=Path(output_path),
                    preset=preset,
                )

            size_after = result["size_after"]
            size_before = result["size_before"]
            ratio = result["ratio"]

            if size_after > MAX_OUTPUT_SIZE:
                await callback.message.answer(
                    t("compress.error_too_big", lang),
                    reply_markup=get_back_keyboard(lang),
                    parse_mode="HTML",
                )
                return

            ratio_pct = int(round(ratio * 100))
            caption_key = "compress.done_video" if media_type == "video" else "compress.done_photo"
            caption = t(
                caption_key, lang,
                size_before=_fmt_size(size_before),
                size_after=_fmt_size(size_after),
                ratio=ratio_pct,
            )
            if ratio > 0.9:
                caption = caption + "\n\n" + t("compress.already_small", lang)
            if settings.bot_username:
                caption = caption + "\n\n" + t(
                    "compress.ad_caption", lang, bot_username=settings.bot_username,
                )

            # отправка
            success = False
            if media_type == "video":
                try:
                    await callback.message.answer_video(
                        video=FSInputFile(output_path),
                        caption=caption,
                        parse_mode="HTML",
                        supports_streaming=True,
                    )
                    success = True
                except Exception as exc:
                    logger.exception("send_video: %s", exc)
                    try:
                        await callback.message.answer_document(
                            document=FSInputFile(output_path),
                            caption=caption,
                            parse_mode="HTML",
                        )
                        success = True
                    except Exception as exc2:
                        logger.exception("send_document fallback: %s", exc2)
                        await callback.message.answer(
                            t("error.generic", lang), parse_mode="HTML",
                        )
            else:
                try:
                    await callback.message.answer_photo(
                        photo=FSInputFile(output_path),
                        caption=caption,
                        parse_mode="HTML",
                    )
                    success = True
                except Exception as exc:
                    logger.exception("send_photo: %s", exc)
                    try:
                        await callback.message.answer_document(
                            document=FSInputFile(output_path),
                            caption=caption,
                            parse_mode="HTML",
                        )
                        success = True
                    except Exception as exc2:
                        logger.exception("send_document(photo) fallback: %s", exc2)
                        await callback.message.answer(
                            t("error.generic", lang), parse_mode="HTML",
                        )

            if success:
                async with async_session() as session:
                    await increment_user_compress_count(session, callback.from_user.id)

                # после удачной отправки шлём главное меню отдельным сообщением
                try:
                    await callback.message.answer(
                        t("start.welcome", lang, name=callback.from_user.first_name),
                        reply_markup=get_start_keyboard(
                            user_id=callback.from_user.id, lang=lang,
                        ),
                        parse_mode="HTML",
                    )
                except Exception:
                    pass

        except CompressorError as exc:
            category = classify_error(exc)
            logger.warning("compress: %s (%s)", exc, category)
            msg_key = {
                "file_too_large": "compress.error_too_big",
                "unsupported_format": "compress.error_unsupported",
                "ffmpeg_error": "compress.error_ffmpeg",
                "timeout": "compress.error_ffmpeg",
            }.get(category, "compress.error_ffmpeg")
            try:
                await callback.message.answer(
                    t(msg_key, lang),
                    reply_markup=get_back_keyboard(lang),
                    parse_mode="HTML",
                )
            except Exception:
                pass
        except Exception as exc:
            logger.exception("compress: неизвестная ошибка: %s", exc)
            try:
                await callback.message.answer(
                    t("error.generic", lang),
                    reply_markup=get_back_keyboard(lang),
                    parse_mode="HTML",
                )
            except Exception:
                pass
        finally:
            # CRITICAL: всегда чистим tmp_dir и FSM — Local Bot API ничего не удаляет
            await cleanup_state(state)

    # после выхода из async with lock — удаляем lock из словаря (cleanup _user_locks)
    user_lock = _user_locks.get(callback.from_user.id)
    if user_lock is not None and not user_lock.locked():
        _user_locks.pop(callback.from_user.id, None)


# ---------- отмена ----------

@router.callback_query(F.data == "compress_cancel")
async def compress_cancel_callback(
    callback: CallbackQuery, state: FSMContext,
) -> None:
    lang = await _get_lang(callback.from_user.id)
    current = await state.get_state()

    if current == CompressStates.processing.state:
        await callback.answer(t("compress.busy", lang), show_alert=True)
        return

    await cleanup_state(state)
    try:
        await callback.message.edit_text(
            t("compress.cancelled", lang),
            reply_markup=get_start_keyboard(
                user_id=callback.from_user.id, lang=lang,
            ),
            parse_mode="HTML",
        )
    except Exception:
        await callback.message.answer(
            t("compress.cancelled", lang),
            reply_markup=get_start_keyboard(
                user_id=callback.from_user.id, lang=lang,
            ),
            parse_mode="HTML",
        )
    await callback.answer()


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    lang = await _get_lang(message.from_user.id)
    current = await state.get_state()

    if current == CompressStates.processing.state:
        await message.answer(t("compress.busy", lang), parse_mode="HTML")
        return

    await cleanup_state(state)
    await message.answer(
        t("compress.cancelled", lang),
        reply_markup=get_start_keyboard(
            user_id=message.from_user.id, lang=lang,
        ),
        parse_mode="HTML",
    )


# ---------- подсказка на текст в waiting_file ----------

@router.message(CompressStates.waiting_file, F.text)
async def _prompt_file(message: Message, state: FSMContext) -> None:
    lang = await _get_lang(message.from_user.id)
    if message.text and message.text.startswith("/"):
        return
    await message.answer(
        t("compress.send_file", lang),
        reply_markup=get_compress_cancel_keyboard(lang),
        parse_mode="HTML",
    )
