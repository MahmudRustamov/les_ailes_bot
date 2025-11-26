from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from django.utils.translation import gettext as _
from bot.utils.city import get_all_cities


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



async def get_cities_keyboard(lang: str):
    cities = await get_all_cities()
    keyboards = ReplyKeyboardBuilder()
    name_field = f"name_{lang}"

    if cities:
        for city in cities:
            city_name = getattr(city, name_field, city.name)
            keyboards.button(text=city_name)
    else:
        back_text_map = {
            "uz": "⬅️ Orqaga",
            "en": "⬅️ Back",
        }
        keyboards.button(text=back_text_map.get(lang, "⬅️ Back"))

    keyboards.adjust(2)
    return keyboards.as_markup(resize_keyboard=True)


main_menu_en = ReplyKeyboardMarkup(
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
    ], resize_keyboard=True
)


phone_number = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Sharing/Ulashish", request_contact=True)
    ]], resize_keyboard=True
)

location_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Share/Ulashish", request_location=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👤 Profile"),
            KeyboardButton(text="⚙️ Settings"),
        ]
    ], resize_keyboard=True
)

# languages_keyboard = {
#     "en": main_menu_en,
#     "uz": main_menu_uz,
# }


main_menu_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Buyurtma")],
        [KeyboardButton(text="📖 Mening buyurtmalarim")],
        [
            KeyboardButton(text="⚙️ Sozlamalar"),
            KeyboardButton(text="🔥 Aksiya va chegirmalar")
        ],
        [
            KeyboardButton(text="🙋🏻‍♂️ Jamoamizga qo'shilish"),
            KeyboardButton(text="☎️ Aloqa"),
        ]
    ], resize_keyboard=True
)


order_en = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🏃 Take away"),
            KeyboardButton(text="🚙 Delivery")
        ],
        [KeyboardButton(text="⬅️ Back")]
    ],  resize_keyboard=True
)

order_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🏃 Olib ketish"),
            KeyboardButton(text="🚙 Yetkazib berish")
        ],
        [KeyboardButton(text="⬅️ Orqaga")]
    ],  resize_keyboard=True
)


take_away_button_en = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Back"),
            KeyboardButton(text="📍Determine nearest branch")
        ],
        [
            KeyboardButton(text="Order here 🌐"),
            KeyboardButton(text="Select branch")
        ],

    ], resize_keyboard=True
)

take_away_button_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⬅️ Orqaga"),
            KeyboardButton(text="📍Eng yaqin filialni aniqlash")
        ],
        [
            KeyboardButton(text="Bu yerda buyurtma berish 🌐"),
            KeyboardButton(text="Filialni tanlash")
        ],
    ], resize_keyboard=True
)

contact_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💬 Biz bilan aloqaga chiqing"),
            KeyboardButton(text="✍️ Fikr bildirish")
        ],
        [
            KeyboardButton(text="⬅️ Orqaga"),
        ],

    ], resize_keyboard=True
)

contact_en = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💬 Text us"),
            KeyboardButton(text="✍️ Leave a feedback")
        ],
        [
            KeyboardButton(text="⬅️ Back"),
        ],

    ], resize_keyboard=True
)

delivery_en = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍Determine nearest branch")
        ],
        [
            KeyboardButton(text="⬅️ Back"),
            KeyboardButton(text="🗺 My addresses")
        ],

    ], resize_keyboard=True, one_time_keyboard=True
)

delivery_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍Eng yaqin filialni aniqlash")
        ],
        [
            KeyboardButton(text="⬅️ Orqaga"),
            KeyboardButton(text="🗺 Mening manzillarim")
        ],

    ], resize_keyboard=True, one_time_keyboard=True
)

user_settings_en = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✏️ Change name"), KeyboardButton(text="📱Change number")],
        [KeyboardButton(text="🏙 Change city"), KeyboardButton(text="🇬🇧 Change language")],
        [KeyboardButton(text="ℹ️ Branch information"), KeyboardButton(text=" 📄Public offer")],
        [KeyboardButton(text="⬅️ Back")]
    ],
    resize_keyboard=True
)

user_settings_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✏️ Ismni o'zgartirish"), KeyboardButton(text="📱 Raqamni o'zgartirish")],
        [KeyboardButton(text="🏙 Shaharni o'zgartirish"), KeyboardButton(text="🇺🇿 Tilni o'zgartirish")],
        [KeyboardButton(text="ℹ️ Filial ma'lumotlari"), KeyboardButton(text="📄 Jamoat taklifi")],
        [KeyboardButton(text="⬅️ Orqaga")]
    ],
    resize_keyboard=True
)
