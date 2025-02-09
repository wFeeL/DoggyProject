import logging

from aiogram import Router, Bot, F
from aiogram.client.bot import DefaultBotProperties
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from telegram_bot import text_message, callback_text
from telegram_bot.config_reader import config
from telegram_bot.keyboards.inline_markup import get_start_keyboard, get_about_keyboard, get_form_keyboard

router = Router()  # Create a router for bot's commands
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Commander')


# COMMANDS
# Command: /start
@router.message(Command('start'))
async def send_start(message: Message) -> None:
    await message.answer(text=text_message.START_MESSAGE.format(name=message.chat.first_name), reply_markup=get_start_keyboard())

# Command: /contact
@router.message(Command('contact'))
async def send_contact(message: Message) -> None:
    await message.answer(text=text_message.CONTACT, disable_web_page_preview=True)

# Command: /about
@router.message(Command('about'))
async def send_about(message: Message) -> None:
    await message.answer(text=text_message.ABOUT, reply_markup=get_about_keyboard(), disable_web_page_preview=True)

# Command: /form
@router.message(Command('form'))
async def send_form(message: Message) -> None:
    await message.answer(text=text_message.FORM, reply_markup=get_form_keyboard())

# CALLBACKS
@router.callback_query(lambda call: call.data in list(callback_text.CALLBACK.values()))
async def handle_callback(callback: CallbackQuery, **kwargs) -> None:
    try:
        await callback.message.delete()

    except TelegramBadRequest as error:
        logger.info(error.message)
    await callback_text.call_function_from_callback(callback, **kwargs)


@router.callback_query(F.data == 'delete_message')
async def delete_message(callback: CallbackQuery) -> None:
    try:
        await callback.message.delete()

    except TelegramBadRequest as error:
        logger.info(error.message)