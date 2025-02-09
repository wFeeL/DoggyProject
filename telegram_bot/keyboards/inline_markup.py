from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from telegram_bot import callback_text


def get_form_button(text='✏️ Заполнить анкету') -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text=text, callback_data=callback_text.CALLBACK['send_form'])]
    return button

def get_site_button(text='ℹ️ Сайт') -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text=text, url='https://doggy-logy.ru')]
    return button

def get_telegram_channel_button(text='👥 Сообщество') -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text=text, url='https://t.me/DoggyLogyChannel')]
    return button

def get_skip_photo_button(text='Пропустить выбор фото ⏩') -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text=text, callback_data='skip_photos')]
    return button

def get_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(*get_site_button(), *get_telegram_channel_button(), *get_form_button())
    builder.adjust(2, 1)
    return builder.as_markup()

def get_about_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(*get_site_button(), *get_form_button())
    builder.adjust(1, 1)
    return builder.as_markup()

def get_form_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='✅ Начать анкетирование', callback_data='start_form'),)
    return builder.as_markup()

def get_delete_message_button(text='👀 Скрыть') -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text=text, callback_data='delete_message')]
    return button

def get_stop_form_keyboard(is_skip_file: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='⛔ Остановить анкетирование', callback_data='cancel_form'),
                *get_delete_message_button())
    if is_skip_file:
        builder.add(*get_skip_photo_button())
    builder.adjust(1, 1)
    return builder.as_markup()

def get_skip_photos_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[get_skip_photo_button()])
    return markup

def get_send_data_keyboard(media_group: tuple[int, int] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if media_group is None:
        builder.row(InlineKeyboardButton(text='✅ Отправить данные', callback_data="{" + f"\"action\":\"send\"" + "}"),
                    InlineKeyboardButton(text='🚫 Отмена', callback_data="{" + f"\"action\":\"cancel\"" + "}"))
    else:
        first_message_id = media_group[0]
        last_message_id = first_message_id + media_group[1]
        builder.row(InlineKeyboardButton(text='✅ Отправить данные', callback_data="{" + f"\"action\":\"send\",\"first_msg\":\"{first_message_id}\","
                                    f"\"last_msg\":\"{last_message_id}\"" + "}"),
                    InlineKeyboardButton(text='🚫 Отмена', callback_data="{" + f"\"action\":\"cancel\",\"first_msg\":\"{first_message_id}\","
                                    f"\"last_msg\":\"{last_message_id}\"" + "}"))
    return builder.as_markup()