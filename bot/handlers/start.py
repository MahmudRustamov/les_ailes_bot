from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from django.utils.translation import gettext as _
from bot.keyboards.builder import default_keyboard_builder
from bot.keyboards.default.user import get_user_main_keyboards
from bot.keyboards.inline.user import get_language_keyboard
from bot.states.auth import RegisterState
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


@router.callback_query(F.data.startswith("lang_"), RegisterState.language)
async def change_language(call: CallbackQuery, state: FSMContext):
    """Handle language change"""
    language_code = call.data.split("_")[1]
    user_id = call.from_user.id

    # Update user's language (await async function)
    await set_user_language(user_id, language_code)

    cities = await get_all_cities()
    text = _("Please choose the city")
    await call.message.answer(
        text,
        reply_markup=await default_keyboard_builder(
            message=call.message, keyboards=cities, column_name='name'
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
async def cmd_language(message: Message):
    """Language selection command"""
    text = _("🌐 Please select your language:")
    await message.answer(text, reply_markup=await get_language_keyboard())


@router.message(Command("photo"))
async def photos(message: Message):
    products = await get_all_products()
    for product in products:
        await message.answer_photo(
            photo=product.file_id,
            caption=product.caption
        )

