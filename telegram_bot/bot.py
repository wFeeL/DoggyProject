import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from telegram_bot.handlers import bot_commands
from telegram_bot.config_reader import config
from telegram_bot.states import form

# Getting logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create a telegram_bot by token
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main() -> None:
    # Include all routers
    routers = [bot_commands.router, form.router]
    dp.include_routers(*routers)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
