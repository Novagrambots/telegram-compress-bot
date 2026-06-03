"""Утилита для установки персонального меню команд юзеру"""
import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat

from bot.i18n import t

logger = logging.getLogger(__name__)

# список команд в нужном порядке (без доменных команд типа /trim)
MENU_COMMANDS = ["start", "menu", "profile", "help", "language"]


async def set_user_commands(bot: Bot, user_id: int, lang: str) -> None:
    """Устанавливает персональное меню команд для конкретного юзера на его языке"""
    commands = [
        BotCommand(command=cmd, description=t(f"cmd.{cmd}", lang))
        for cmd in MENU_COMMANDS
    ]
    try:
        await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeChat(chat_id=user_id),
        )
    except Exception as e:
        # не критично — просто логируем
        logger.warning("Не удалось установить команды для %s: %s", user_id, e)


async def set_default_commands(bot: Bot) -> None:
    """Устанавливает глобальные команды для каждого языка.
    Telegram сам покажет их юзеру, основываясь на языке его приложения,
    ЕЩЁ ДО ТОГО как юзер нажмёт /start.
    """
    for lang in ["ru", "en", "uz"]:
        # для uz используем uz_latn (латиница)
        i18n_lang = "uz_latn" if lang == "uz" else lang
        commands = [
            BotCommand(command=cmd, description=t(f"cmd.{cmd}", i18n_lang))
            for cmd in MENU_COMMANDS
        ]
        # Отправляем в Telegram с указанием language_code
        await bot.set_my_commands(commands=commands, language_code=lang)

    # Резервный дефолт, если язык приложения вообще другой (например, испанский)
    fallback = [
        BotCommand(command=cmd, description=t(f"cmd.{cmd}", "en"))
        for cmd in MENU_COMMANDS
    ]
    await bot.set_my_commands(commands=fallback)
