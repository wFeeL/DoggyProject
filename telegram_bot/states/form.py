import json
import re

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.client.bot import DefaultBotProperties
from aiogram.client.session.base import TelegramForbiddenError
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_media_photo import InputMediaPhoto

from telegram_bot import text_message
from telegram_bot.config_reader import config
from telegram_bot.handlers.bot_commands import logger
from telegram_bot.keyboards.inline_markup import get_stop_form_keyboard, get_skip_photos_keyboard, \
    get_send_data_keyboard
from telegram_bot.middleware.album_middleware import AlbumMiddleware


class Form(StatesGroup):
    fullname = State()
    phone_number = State()
    city = State()
    dog_breed = State()
    dog_age = State()
    transport_question = State()
    shooting_day_question = State()
    dog_skills = State()
    file_id = State()
    message_id = State()
    none_state = State()


router = Router()
router.message.middleware(AlbumMiddleware())
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


@router.callback_query(F.data == 'start_form')
async def handle_start_form(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(text='Введите ваше ФИО:')
    await state.set_state(Form.fullname)


@router.message(Form.fullname)
async def process_fullname(message: Message, state: FSMContext) -> None:
    await state.update_data(fullname=message.text)
    await message.answer(text='Введите ваш номер телефона:')
    await state.set_state(Form.phone_number)


@router.message(Form.phone_number)
async def process_phone_number(message: Message, state: FSMContext) -> None:
    try:
        phone_number = message.text.strip()
        cleaned_number = re.sub(r'[\s\(\)\-]', '', phone_number)

        if cleaned_number.startswith('+7') and len(cleaned_number) == 12 and cleaned_number[1:].isdigit():
            valid_number = cleaned_number
        elif cleaned_number.startswith('8') and len(cleaned_number) == 11 and cleaned_number.isdigit():
            valid_number = '+7' + cleaned_number[1:]
        elif cleaned_number.startswith('7') and len(cleaned_number) == 11 and cleaned_number.isdigit():
            valid_number = '+' + cleaned_number
        else:
            raise ValueError

        await state.update_data(phone_number=valid_number)
        await message.answer(text='Введите город:')
        await state.set_state(Form.city)

    except ValueError:
        await message.answer(
            '🚫 Вы ввели некорректный номер телефона!\n'
            '✅ Используйте формат: +79123456789 или 89123456789\n'
            'Попробуйте еще раз.',
            reply_markup=get_stop_form_keyboard()
        )


@router.message(Form.city)
async def process_city(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    await message.answer(text='Введите породу питомца:')
    await state.set_state(Form.dog_breed)


@router.message(Form.dog_breed)
async def process_dog_breed(message: Message, state: FSMContext) -> None:
    await state.update_data(dog_breed=message.text)
    await message.answer(text='Введите возраст питомца:')
    await state.set_state(Form.dog_age)


@router.message(Form.dog_age)
async def process_dog_age(message: Message, state: FSMContext) -> None:
    await state.update_data(dog_age=message.text)
    await message.answer(text='Как питомец переносит поездки на транспорте? Как можете перемещаться по городу?')
    await state.set_state(Form.transport_question)


@router.message(Form.transport_question)
async def process_transport_question(message: Message, state: FSMContext) -> None:
    await state.update_data(transport_question=message.text)
    await message.answer(text='Можете ли выделить по необходимости день для съемки?')
    await state.set_state(Form.shooting_day_question)


@router.message(Form.shooting_day_question)
async def process_shooting_day_question(message: Message, state: FSMContext) -> None:
    await state.update_data(shooting_day_question=message.text)
    await message.answer(text='Опишите особенности и навыки вашего питомца:')
    await state.set_state(Form.dog_skills)


@router.message(Form.dog_skills)
async def process_dog_skills(message: Message, state: FSMContext) -> None:
    await state.update_data(dog_skills=message.text)
    await message.answer(text='Отправьте фотографию вашего питомца:', reply_markup=get_skip_photos_keyboard())
    await state.set_state(Form.file_id)


@router.message(Form.file_id)
async def process_dog_photos(message: Message, state: FSMContext, album: list = None) -> None:
    try:
        if message.document:
            raise TypeError
        if message.media_group_id:
            await state.update_data(file_id='None')
        else:
            file = await bot.get_file(message.photo[0].file_id)
            await state.update_data(file_id=file.file_id)
        await send_data(message, state, album)
    except TypeError:
        await message.answer('🚫 Вы отправили некорректный файл!\nПопробуйте еще раз.',
                             reply_markup=get_stop_form_keyboard(is_skip_file=True))


async def send_data(message: Message, state: FSMContext, album: list = None) -> None:
    try:
        data = await state.get_data()
        file_id = data['file_id']
        await state.set_state(Form.none_state)
        text = text_message.DATA_TO_SEND.format(**data)
        markup = get_send_data_keyboard()
        if file_id != 'None':
            message = await bot.send_photo(caption=text, reply_markup=markup, photo=file_id, chat_id=message.chat.id)
            message_id = message.message_id

        elif album is not None and len(album) > 0:
            photos = list(map(lambda elem: elem.photo[0].file_id, album))
            first_photo = [InputMediaPhoto(media=photos[0], caption=text)]
            media_group = first_photo + list(map(lambda elem: InputMediaPhoto(media=elem), photos[1:]))
            media_group = await bot.send_media_group(chat_id=message.chat.id, media=media_group)
            message_id = media_group[0].message_id
            media_group_id, media_group_len = message_id, len(media_group)

            markup = get_send_data_keyboard(media_group=(media_group_id, media_group_len))
            await message.answer(text=text_message.CHOOSE_ACTION, reply_markup=markup)

        else:
            message = await message.answer(text=text, reply_markup=markup)
            message_id = message.message_id

        await state.update_data(message_id=message_id)

    except KeyError:
        await message.answer(text=text_message.INCORRECT_REQUEST)
        await state.clear()


@router.callback_query(F.data == 'skip_photos')
async def skip_sending_photos(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(file_id='None')
    await callback.message.delete()
    await send_data(callback.message, state)


@router.callback_query(F.data == 'cancel_form')
async def cancel_send_data(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text_message.CANCEL_FORM)


@router.callback_query(lambda call: 'send' in call.data or 'cancel' in call.data)
async def send_data_to_admin(callback: CallbackQuery, state: FSMContext) -> None:
    json_data = json.loads(callback.data)
    admin_chat_id = config.admin_telegram_id
    if json_data['action'] == 'send':
        try:
            first_message = int(json_data['first_msg'])
            last_message = int(json_data['last_msg'])
            message_ids = list(range(first_message, last_message))

            await bot.forward_messages(chat_id=admin_chat_id, from_chat_id=callback.message.chat.id,
                                       message_ids=message_ids)
            await bot.delete_messages(chat_id=callback.message.chat.id, message_ids=message_ids)

        except KeyError:
            data = await state.get_data()
            message_id = data['message_id']
            await bot.forward_message(chat_id=admin_chat_id, from_chat_id=callback.message.chat.id,
                                      message_id=message_id)

        except TelegramBadRequest as error:
            logger.info(error.message)

        except TelegramForbiddenError:
            logger.error('Bot was blocked by the user.')

        await callback.message.answer(text=text_message.SUCCESS_FORM)
    else:
        await callback.message.answer(text=text_message.CANCEL_SEND)
    await callback.message.delete()
    await state.clear()
