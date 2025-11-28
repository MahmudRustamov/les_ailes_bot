from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.utils.translation import get_user_language


async def default_keyboard_builder(
        column_name: str,
        message: Message | CallbackQuery,
        keyboards: list, row_size=2, back_button=False,
        lang=None
):
    lang = lang if lang else await get_user_language(user_id=message.chat.id)
    builder = ReplyKeyboardBuilder()
    for keyboard in keyboards:
        builder.button(
            text=getattr(keyboard, f'{column_name}_{lang}')
        )

    if back_button:
        builder.button(text="⬅️ Back")

    builder.adjust(row_size)
    return builder.as_markup(resize_keyboard=True)