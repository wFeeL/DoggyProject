import json

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
    name = State()
    city = State()
    species_breed = State()
    gender = State()
    birth_date = State()
    transport_question = State()
    shooting_day_question = State()
    fears = State()
    skills = State()
    shooting_experience = State()
    contact = State()
    file_id = State()
    message_id = State()
    none_state = State()


router = Router()
router.message.middleware(AlbumMiddleware())
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


@router.callback_query(F.data == 'start_form')
async def handle_start_form(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(text=text_message.QUESTION_NAME)
    await state.set_state(Form.name)


@router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer(text=text_message.QUESTION_CITY)
    await state.set_state(Form.city)


@router.message(Form.city)
async def process_city(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    await message.answer(text=text_message.QUESTION_SPECIES_BREED)
    await state.set_state(Form.species_breed)


@router.message(Form.species_breed)
async def process_species_breed(message: Message, state: FSMContext) -> None:
    await state.update_data(species_breed=message.text)
    await message.answer(text=text_message.QUESTION_GENDER)
    await state.set_state(Form.gender)


@router.message(Form.gender)
async def process_gender(message: Message, state: FSMContext) -> None:
    await state.update_data(gender=message.text)
    await message.answer(text=text_message.QUESTION_BIRTH_DATE)
    await state.set_state(Form.birth_date)


@router.message(Form.birth_date)
async def process_birth_date(message: Message, state: FSMContext) -> None:
    await state.update_data(birth_date=message.text)
    await message.answer(text=text_message.QUESTION_TRANSPORT)
    await state.set_state(Form.transport_question)


@router.message(Form.transport_question)
async def process_transport_question(message: Message, state: FSMContext) -> None:
    await state.update_data(transport_question=message.text)
    await message.answer(text=text_message.QUESTION_SHOOTING_DAY)
    await state.set_state(Form.shooting_day_question)


@router.message(Form.shooting_day_question)
async def process_shooting_day_question(message: Message, state: FSMContext) -> None:
    await state.update_data(shooting_day_question=message.text)
    await message.answer(text=text_message.QUESTION_FEARS)
    await state.set_state(Form.fears)


@router.message(Form.fears)
async def process_fears(message: Message, state: FSMContext) -> None:
    await state.update_data(fears=message.text)
    await message.answer(text=text_message.QUESTION_SKILLS)
    await state.set_state(Form.skills)


@router.message(Form.skills)
async def process_skills(message: Message, state: FSMContext) -> None:
    await state.update_data(skills=message.text)
    await message.answer(text=text_message.QUESTION_EXPERIENCE)
    await state.set_state(Form.shooting_experience)


@router.message(Form.shooting_experience)
async def process_shooting_experience(message: Message, state: FSMContext) -> None:
    await state.update_data(shooting_experience=message.text)
    await message.answer(text=text_message.QUESTION_CONTACT)
    await state.set_state(Form.contact)


@router.message(Form.contact)
async def process_contact(message: Message, state: FSMContext) -> None:
    await state.update_data(contact=message.text)
    await message.answer(text=text_message.QUESTION_PHOTO, reply_markup=get_skip_photos_keyboard())
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
    admin_chat_ids = config.admin_telegram_ids
    if json_data['action'] == 'send':
        try:
            first_message = int(json_data['first_msg'])
            last_message = int(json_data['last_msg'])
            message_ids = list(range(first_message, last_message))
            print(message_ids)

            for admin_chat_id in admin_chat_ids:
                await bot.forward_messages(chat_id=admin_chat_id, from_chat_id=callback.message.chat.id,
                                           message_ids=message_ids)
            await bot.delete_messages(chat_id=callback.message.chat.id, message_ids=message_ids)

        except KeyError:
            data = await state.get_data()
            message_id = [data['message_id']]
            for admin_chat_id in admin_chat_ids:
                await bot.forward_messages(chat_id=admin_chat_id, from_chat_id=callback.message.chat.id,
                                           message_ids=message_id)

        except TelegramBadRequest as error:
            logger.info(error.message)

        except TelegramForbiddenError:
            logger.error('Bot was blocked by the user.')

        await callback.message.answer(text=text_message.SUCCESS_FORM)
    else:
        await callback.message.answer(text=text_message.CANCEL_SEND)
    await callback.message.delete()
    await state.clear()
