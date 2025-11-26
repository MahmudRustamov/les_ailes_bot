from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_language_inline_keyboard():
    """Keyboard for language selection"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en"),
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
        ]
    ])
    return keyboard


