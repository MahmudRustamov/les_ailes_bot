from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _


async def get_language_keyboard():
    """Keyboard for language selection"""
    languages = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🇺🇿 O'zbekcha"),
                KeyboardButton(text="🇺🇸 English"),
            ]
        ], resize_keyboard=True
    )
    return languages


async def get_user_main_keyboards() -> ReplyKeyboardMarkup:
    """
    Translatable main keyboard menu (English text for gettext).
    """
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text=_("🛍 Order"))],
            [KeyboardButton(text=_("📖 My orders"))],
            [
                KeyboardButton(text=_("⚙️Settings")),
                KeyboardButton(text=_("🔥 Promotions"))
            ],
            [
                KeyboardButton(text=_("🙋🏻‍♂️ Join to our team")),
                KeyboardButton(text=_("☎️ Contact")),
            ]
        ]
    )

    return keyboard


phone_number = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text=_("📱Share my phone number"), request_contact=True)
    ]], resize_keyboard=True, one_time_keyboard=True
)

location_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Share my location", request_location=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


async def user_settings_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text=_("✍️ Change name")), KeyboardButton(text=_("📱Change number"))],
            [KeyboardButton(text=_("🏙 Change city")), KeyboardButton(text=_("🇬🇧 Change language"))],
            [KeyboardButton(text=_("ℹ️ Branch information")), KeyboardButton(text=_(" 📄Public offer"))],
            [KeyboardButton(text=_("⬅️ Back"))

            ]
        ],
    )
    return keyboard


async def contact_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("💬 Text us")),
                KeyboardButton(text=_("✍️ Leave a feedback"))
            ],
            [
                KeyboardButton(text=_("⬅️ Back")),
            ],

        ]
    )
    return keyboard

