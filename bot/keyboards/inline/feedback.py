from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.utils.translation import gettext as _



async def get_language_keyboard():
    """Keyboard for language selection"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en"),
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
        ]
    ])
    return keyboard


async def get_rating_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
            # product header
            [InlineKeyboardButton(text=_("Product"), callback_data="header_product")],

            # product row
            [
                InlineKeyboardButton(text="1 😖", callback_data="product_1"),
                InlineKeyboardButton(text="2 ☹️", callback_data="product_2"),
                InlineKeyboardButton(text="3 😕", callback_data="product_3"),
                InlineKeyboardButton(text="4 😐", callback_data="product_4"),
                InlineKeyboardButton(text="5 😍", callback_data="product_5"),
            ],

            # package header
            [InlineKeyboardButton(text=_("Package"), callback_data="header_package")],


            [
                InlineKeyboardButton(text="1 👊", callback_data="package_1"),
                InlineKeyboardButton(text="2 👎", callback_data="package_2"),
                InlineKeyboardButton(text="3 👌", callback_data="package_3"),
                InlineKeyboardButton(text="4 🤙", callback_data="package_4"),
                InlineKeyboardButton(text="5 👍", callback_data="package_5"),
            ],

            # delivery header
            [InlineKeyboardButton(text=_("Delivery"), callback_data="header_delivery")],

            # delivery row
            [
                InlineKeyboardButton(text="1 🐌", callback_data="delivery_1"),
                InlineKeyboardButton(text="2 🐢", callback_data="delivery_2"),
                InlineKeyboardButton(text="3 🚚", callback_data="delivery_3"),
                InlineKeyboardButton(text="4 🏍️", callback_data="delivery_4"),
                InlineKeyboardButton(text="5 🚀", callback_data="delivery_5"),
            ],
        ]
    )
    return keyboard
