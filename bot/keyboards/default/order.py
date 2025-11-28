from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _


async def get_order_type_keyboards() -> ReplyKeyboardMarkup:
    """
    Keyboard for choosing order type (take away or delivery).
    """
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="🏃‍♂️" + _(" Take away")),
                KeyboardButton(text="🚙 " + _("Delivery")),
            ],
            [
                KeyboardButton(text="⬅️ " + _("Back")),
            ]
        ]
    )

    return keyboard


async def get_takeaway_keyboards() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="⬅️ " + _("Back")),
            ],
            [
                KeyboardButton(text="📍 " + _("Determine nearest branch"), request_location=True),
            ],
            [
                KeyboardButton(text="🌐 " + _("Order here")),
                KeyboardButton(text=_("Select branch")),
            ]
        ]
    )


async def get_delivery_keyboards() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="📍 " + _("Determine nearest branch"), request_location=True),
            ],
            [
                KeyboardButton(text="⬅️ " + _("Back")),
                KeyboardButton(text="🗺 " + _("My addresses"))
            ]
        ]
    )