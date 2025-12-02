from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from django.utils.translation import gettext as _
from bot.keyboards.builder import default_keyboard_builder
from bot.keyboards.default.user import get_user_main_keyboards, get_language_keyboard, user_settings_keyboard
from bot.keyboards.inline.user import get_language_inline_keyboards
from bot.states.auth import RegisterState, UpdateState
from bot.states.order import OrderState
from bot.utils.city import get_all_cities, get_city
from bot.utils.product import get_all_products
from bot.utils.translation import set_user_language, get_or_create_user
from bot.utils.user import partial_update_user

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Start command handler"""
    await state.set_state(RegisterState.language)
    user = message.from_user

    # Create or update user in database (await async function)
    user, created = await get_or_create_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    if created:
        welcome_text = """
Assalomu alaykum! Les Ailes yetkazib berish xizmatiga xush kelibsiz.

Здравствуйте! Добро пожаловать в службу доставки Les Ailes.

Hello! Welcome to Les Ailes delivery service.
"""
        await message.answer(
            welcome_text,
            reply_markup=await get_language_keyboard()
        )
    else:
        cities = await get_all_cities()
        text = _("Please select the city")
        await message.answer(
            text,
            reply_markup=await default_keyboard_builder(
                message=message, keyboards=cities, column_name='name'
            )
        )
        await state.set_state(RegisterState.city)


@router.message(F.text.in_(['🇺🇸 English', "🇺🇿 O'zbekcha"]), RegisterState.language)
async def language_handler(message: Message, state: FSMContext):
    """Handle language change"""
    user_id = message.from_user.id
    if message.text == "🇺🇸 English":
        language_code = "en"
        await set_user_language(user_id, language_code)
    elif message.text == "🇺🇿 O'zbekcha":
        language_code = "uz"
        await set_user_language(user_id, language_code)

    cities = await get_all_cities()
    text = _("Please choose the city")
    await message.answer(
        text,
        reply_markup=await default_keyboard_builder(
            message=message, keyboards=cities, column_name='name'
        )
    )
    await state.set_state(RegisterState.city)


@router.message(RegisterState.city)
async def get_city_handler(message: Message, state: FSMContext):
    city = await get_city(city_name=message.text)

    await partial_update_user(data={
        'city_id': city.id
    }, user_id=message.chat.id)

    text = _('Welcome to main menu 😊')
    await message.answer(text=text, reply_markup=await get_user_main_keyboards())
    await state.clear()





# -----------------------------------------------------
@router.message(Command("help"))
async def cmd_help(message: Message):
    """Help command with translated text"""
    help_text = _(
        "📚 <b>Available Commands:</b>\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/language - Change language\n\n"
        "If you have any questions, feel free to ask!"
    )

    await message.answer(help_text, parse_mode="HTML")


@router.message(Command("language"))
async def cmd_language(message: Message, state: FSMContext):
    text = _("🌐 Please select your language:")
    await message.answer(text, reply_markup=await get_language_inline_keyboards())


@router.callback_query(F.data.startswith("lang_"))
async def command_language(call: CallbackQuery):
    language_code = call.data.split("_")[1]
    user_id = call.from_user.id

    await set_user_language(user_id, language_code)

    text = _("Language successfully updated ✅"),

    await call.message.answer(
        _("Language successfully updated ✅")
    )


@router.message(F.text.in_(['🇺🇸 English', "🇺🇿 O'zbekcha"]), UpdateState.change_lang)
async def settings_change_language(message: Message, state: FSMContext):
    """Handle language change from settings menu"""
    user_id = message.from_user.id

    if message.text == "🇺🇸 English":
        language_code = "en"
    elif message.text == "🇺🇿 O'zbekcha":
        language_code = "uz"
    else:
        return

    await set_user_language(user_id, language_code)

    await message.answer(
        _("Language successfully updated ✅"),
        reply_markup=await user_settings_keyboard()
    )
    await state.clear()



@router.message(Command("photo"))
async def photos(message: Message):
    products = await get_all_products()
    for product in products:
        await message.answer_photo(
            photo=product.file_id,
            caption=product.caption
        )

