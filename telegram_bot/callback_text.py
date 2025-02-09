from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import CallbackQuery

from telegram_bot.handlers import bot_commands
from telegram_bot.config_reader import config

CALLBACK = {
    'send_form': 'form',
}

bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


# Call a function from callback data
async def call_function_from_callback(callback: CallbackQuery, **kwargs) -> None:
    for key in list(CALLBACK.keys()):
        if CALLBACK[key] == callback.data:
            func = getattr(bot_commands, key)
            await func(callback.message)
