from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_proceed_button(button_name: str, link: str):
    """Keyboard for language selection"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=button_name, callback_data="proceed_button", url=link),
        ]
    ])
    return keyboard


