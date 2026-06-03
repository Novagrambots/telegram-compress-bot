"""Сервис сжатия медиафайлов: видео (H.265/MP4) и фото (JPEG).

Видео:
  - libx265 c CRF по пресету (low=28, medium=32, high=38)
  - даунскейл и снижение fps только для medium/high и только если исходное больше
  - tag:v hvc1 + faststart — совместимость c iPhone/macOS
  - аудио: AAC 128k
  - asyncio.create_subprocess_exec (НЕ subprocess.run!)
  - семафор: 2 параллельных задачи (H.265 очень CPU-тяжёлый)

Фото:
  - Pillow (блокирующий) — через asyncio.to_thread
  - HEIC через pillow-heif
  - выход всегда JPEG, качество по пресету (85/70/50)
  - RGBA → RGB с белым фоном

Доменная ошибка — CompressorError. Классификатор — classify_error().
"""
from __future__ import annotations

import asyncio
import logging
from io import BytesIO
from pathlib import Path

logger = logging.getLogger(__name__)


class CompressorError(Exception):
    """Доменная ошибка сервиса сжатия."""


# === HEIC support ===
# pillow-heif обязательный — зафиксирован в requirements.txt
import pillow_heif  # type: ignore

pillow_heif.register_heif_opener()


# === Параметры ===

# H.265 настолько CPU-тяжёлый, что больше 2 параллельных задач кладут VPS
_SEMAPHORE = asyncio.Semaphore(2)

# таймауты
_FFMPEG_TIMEOUT = 1800  # 30 минут — крупное видео без CUDA вполне может ехать долго
_FFPROBE_TIMEOUT = 60

# CRF + лимиты разрешения / fps по пресетам видео
_VIDEO_PRESETS: dict[str, dict] = {
    "low":    {"crf": 28, "max_height": None, "max_fps": None},
    "medium": {"crf": 32, "max_height": 720,  "max_fps": 30},
    "high":   {"crf": 38, "max_height": 480,  "max_fps": 30},
}

# качество JPEG по пресетам
_PHOTO_QUALITY: dict[str, int] = {
    "low": 85,
    "medium": 70,
    "high": 50,
}


# ============ ffprobe ============

async def get_media_info(path: Path, kind: str) -> dict:
    """Возвращает метаданные медиафайла.

    Тип определяется по `kind` (приходит из MIME-сообщения), а не угадывается:
    ffprobe видит JPEG как codec_type=video,codec_name=mjpeg,fps=25/1 и фото
    ошибочно классифицировалось бы как видео.

    Для kind="video": {"kind": "video", "duration", "width", "height", "fps"}
    Для kind="photo": {"kind": "photo", "width", "height"}
    """
    p = Path(path)
    if not p.exists():
        raise CompressorError(f"файл не найден: {p}")

    if kind == "photo":
        return await asyncio.to_thread(_probe_photo, p)

    if kind != "video":
        raise CompressorError(f"неизвестный kind: {kind}")

    # видео — ffprobe первого видеопотока и duration
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries",
        "stream=width,height,avg_frame_rate,codec_type:format=duration",
        "-of", "default=nw=1",
        str(p),
    ]
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    except FileNotFoundError as exc:
        raise CompressorError(f"ffprobe не найден: {exc}") from exc

    try:
        stdout, stderr = await asyncio.wait_for(
            process.communicate(), timeout=_FFPROBE_TIMEOUT,
        )
    except asyncio.TimeoutError:
        try:
            process.kill()
            await process.wait()
        except Exception:
            pass
        raise CompressorError("ffprobe timeout")

    if process.returncode != 0:
        err = stderr.decode(errors="replace").strip()
        raise CompressorError(f"ffprobe returncode={process.returncode}: {err[:300]}")

    info: dict[str, str] = {}
    for line in stdout.decode(errors="replace").splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            info[k.strip()] = v.strip()

    width = int(info.get("width", 0) or 0)
    height = int(info.get("height", 0) or 0)
    codec = info.get("codec_type", "")
    duration_raw = info.get("duration", "")
    try:
        duration = float(duration_raw) if duration_raw and duration_raw != "N/A" else 0.0
    except ValueError:
        duration = 0.0

    # avg_frame_rate вида "30000/1001"
    fps = 0.0
    afr = info.get("avg_frame_rate", "")
    if afr and afr != "0/0":
        try:
            if "/" in afr:
                num, _, den = afr.partition("/")
                num_f = float(num)
                den_f = float(den) or 1.0
                fps = num_f / den_f
            else:
                fps = float(afr)
        except (ValueError, ZeroDivisionError):
            fps = 0.0

    return {
        "kind": "video",
        "duration": duration,
        "width": width,
        "height": height,
        "fps": fps,
    }


def _probe_photo(p: Path) -> dict:
    """Синхронный probe фото через Pillow."""
    try:
        from PIL import Image
        with Image.open(p) as img:
            w, h = img.size
        return {"kind": "photo", "width": int(w), "height": int(h)}
    except Exception as exc:
        raise CompressorError(f"не удалось открыть фото: {exc}") from exc


# ============ видео ============

async def compress_video(
    input_path: Path,
    output_path: Path,
    preset: str,
) -> dict:
    """Сжимает видео в MP4/H.265 по пресету.

    Возвращает {"size_before": int, "size_after": int, "ratio": float}.
    """
    if preset not in _VIDEO_PRESETS:
        raise CompressorError(f"неизвестный пресет: {preset!r}")

    inp = Path(input_path)
    out = Path(output_path)
    if not inp.exists():
        raise CompressorError(f"входной файл не найден: {inp}")

    cfg = _VIDEO_PRESETS[preset]
    crf = cfg["crf"]

    # читаем разрешение/fps входа — чтобы решить, нужен ли даунскейл
    info = await get_media_info(inp, kind="video")
    if info.get("kind") != "video":
        raise CompressorError("это не видео")

    src_h = int(info.get("height") or 0)
    src_fps = float(info.get("fps") or 0)

    vf_parts: list[str] = []
    if cfg["max_height"] and src_h and src_h > cfg["max_height"]:
        # уменьшаем только по высоте, ширину пересчитываем (-2 — чётная)
        vf_parts.append(f"scale=-2:{cfg['max_height']}")

    out_fps = None
    if cfg["max_fps"] and src_fps and src_fps > cfg["max_fps"]:
        out_fps = cfg["max_fps"]

    out.parent.mkdir(parents=True, exist_ok=True)

    cmd: list[str] = [
        "ffmpeg",
        "-y",
        "-loglevel", "error",
        "-i", str(inp),
    ]
    if vf_parts:
        cmd += ["-vf", ",".join(vf_parts)]
    if out_fps:
        cmd += ["-r", str(out_fps)]
    cmd += [
        "-c:v", "libx265",
        "-preset", "fast",
        "-crf", str(crf),
        "-tag:v", "hvc1",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        str(out),
    ]

    async with _SEMAPHORE:
        logger.info(
            "ffmpeg: compress_video %s → %s (preset=%s, crf=%s, vf=%s, fps=%s)",
            inp.name, out.name, preset, crf, vf_parts or None, out_fps,
        )
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError as exc:
            raise CompressorError(f"ffmpeg не найден: {exc}") from exc
        except Exception as exc:
            raise CompressorError(f"ffmpeg: ошибка запуска: {exc}") from exc

        try:
            _, stderr = await asyncio.wait_for(
                process.communicate(), timeout=_FFMPEG_TIMEOUT,
            )
        except asyncio.TimeoutError:
            try:
                process.kill()
            except ProcessLookupError:
                pass
            try:
                await process.wait()
            except Exception:
                pass
            try:
                if out.exists():
                    out.unlink()
            except OSError:
                pass
            raise CompressorError("ffmpeg timeout")

        if process.returncode != 0:
            err = stderr.decode(errors="replace").strip()
            try:
                if out.exists():
                    out.unlink()
            except OSError:
                pass
            raise CompressorError(
                f"ffmpeg returncode={process.returncode}: {err[:500]}"
            )

    if not out.exists() or out.stat().st_size == 0:
        raise CompressorError("ffmpeg отработал, но выходной файл пуст")

    size_before = inp.stat().st_size
    size_after = out.stat().st_size
    ratio = (size_after / size_before) if size_before else 1.0

    return {"size_before": size_before, "size_after": size_after, "ratio": ratio}


# ============ фото ============

async def compress_photo(
    input_path: Path,
    output_path: Path,
    preset: str,
) -> dict:
    """Сжимает фото в JPEG через Pillow (в отдельном потоке).

    Возвращает {"size_before", "size_after", "ratio"}.
    """
    if preset not in _PHOTO_QUALITY:
        raise CompressorError(f"неизвестный пресет: {preset!r}")

    inp = Path(input_path)
    out = Path(output_path)
    if not inp.exists():
        raise CompressorError(f"входной файл не найден: {inp}")

    quality = _PHOTO_QUALITY[preset]
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        await asyncio.to_thread(_compress_photo_sync, inp, out, quality)
    except CompressorError:
        raise
    except Exception as exc:
        raise CompressorError(f"pillow: {exc}") from exc

    if not out.exists() or out.stat().st_size == 0:
        raise CompressorError("выходной файл пуст")

    size_before = inp.stat().st_size
    size_after = out.stat().st_size
    ratio = (size_after / size_before) if size_before else 1.0
    return {"size_before": size_before, "size_after": size_after, "ratio": ratio}


def _compress_photo_sync(inp: Path, out: Path, quality: int) -> None:
    """Блокирующий код Pillow — вызывается через asyncio.to_thread."""
    from PIL import Image, ImageOps

    try:
        with Image.open(inp) as img:
            # авто-поворот по EXIF (камеры iPhone часто пишут портреты с rotation)
            img = ImageOps.exif_transpose(img)

            # JPEG не поддерживает альфу — кладём на белый фон
            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                # маска — альфа-канал
                alpha = img.split()[-1]
                background.paste(img.convert("RGB"), mask=alpha)
                img = background
            elif img.mode == "P":
                # палитра — конвертируем в RGB, чтобы не получить артефакты
                img = img.convert("RGB")
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # сначала в буфер — чтобы не оставить битый файл на диске при ошибке
            buf = BytesIO()
            img.save(
                buf,
                format="JPEG",
                quality=quality,
                optimize=True,
                progressive=True,
            )
            out.write_bytes(buf.getvalue())
    except FileNotFoundError as exc:
        raise CompressorError(f"файл не найден: {exc}") from exc


# ============ классификатор ============

def classify_error(exc: BaseException) -> str:
    """Категории: file_too_large / unsupported_format / ffmpeg_error / timeout / unknown."""
    if isinstance(exc, CompressorError):
        msg = str(exc).lower()
        if "timeout" in msg:
            return "timeout"
        if "too large" in msg or "file too large" in msg:
            return "file_too_large"
        if (
            "invalid data" in msg
            or "no such" in msg
            or "not found" in msg
            or "unsupported" in msg
            or "не удалось открыть" in msg
            or "это не видео" in msg
            or "moov atom" in msg
            or "invalid argument" in msg
            or "could not find codec" in msg
        ):
            return "unsupported_format"
        if "ffmpeg" in msg or "ffprobe" in msg or "pillow" in msg:
            return "ffmpeg_error"
        return "ffmpeg_error"
    if isinstance(exc, asyncio.TimeoutError):
        return "timeout"
    name = type(exc).__name__.lower()
    if "timeout" in name:
        return "timeout"
    return "unknown"
