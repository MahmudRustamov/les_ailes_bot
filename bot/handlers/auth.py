from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from django.utils.translation import gettext as _
from bot.keyboards.builder import default_keyboard_builder
from bot.keyboards.default.order import get_delivery_keyboards
from bot.keyboards.default.user import contact_keyboard, user_settings_keyboard, get_language_keyboard, phone_number
from bot.keyboards.inline.feedback import get_rating_keyboard
from bot.keyboards.inline.order import get_proceed_button
from bot.states.auth import UpdateState
from bot.states.order import OrderState
from bot.utils.city import get_all_cities, get_city
from bot.utils.user import partial_update_user

router = Router()


@router.message(F.text.in_(['🗺 My addresses', '🗺 Mening manzillarim']))
async def address_handler(message: Message, state: FSMContext):
    # await state.set_state(OrderState.location)
    # await state.update_data(order_type="delivery")

    text = _("You do not have any saved addresses")
    await message.answer(text=text, reply_markup=await get_delivery_keyboards())


@router.message(F.text.in_(['🙋🏻‍♂️ Join to our team', "🙋🏻‍♂️ Jamoamizga qo'shiling"]))
async def vacancies_handler(message: Message, state: FSMContext):
    text = _("Join our friendly team our friendly team! Click on the button below to fill out the questionnaire right here, without leaving Telegram.")
    await message.answer(text=text, reply_markup=await get_proceed_button(button_name=_("Proceed"), link="https://t.me/myexceptionns"))


@router.message(F.text.in_(['☎️ Contact', "☎️ Biz bilan aloqa"]))
async def contact_button_handler(message: Message, state: FSMContext):
    # await state.set_state(OrderState.location)
    await state.set_state(OrderState.order_type)
    text = _("We will be glad to hear from you. Leave a feedback")
    await message.answer(text=text, reply_markup=await contact_keyboard())


@router.message(F.text.in_(['💬 Text us', "💬 Biz bilan aloqaga chiqing"]))
async def support_button_handler(message: Message, state: FSMContext):
    text = _("If you have any questions, feel free to text us")
    await message.answer(text=text, reply_markup=await get_proceed_button(button_name=_("💬 Text us"), link="https://t.me/myexceptionns"))


@router.message(F.text.in_(['⚙️Settings', '⚙️Sozlamalar']))
async def settings_handler(message: Message, state: FSMContext):
    await state.set_state(OrderState.order_type)
    text = _("Choose an action:")
    await message.answer(text=text, reply_markup=await user_settings_keyboard())


@router.message(F.text.in_(['ℹ️ Branch information', "ℹ️ Filallar haqida ma'lumotlar"]))
async def branches_handler(message: Message, state: FSMContext):
    await state.set_state(OrderState.order_type)
    text = _("No branches found")
    await message.answer(text=text, reply_markup=await user_settings_keyboard())


@router.message(F.text.in_(['📄Public offer', '📄 Ommaviy taklif']))
async def offers_handler(message: Message, state: FSMContext):
    await state.set_state(OrderState.order_type)
    text = "https://telegra.ph/Publichnaya-oferta-Chopar-Pizza-05-21"
    await message.answer(text=text, reply_markup=await user_settings_keyboard())


@router.message(F.text.in_(['✍️ Change name', "✍️ Ismni o'zgartirish"]))
async def update_name_handler(message: Message, state: FSMContext):
    text = "Please enter your new name:"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(UpdateState.change_name)


@router.message(UpdateState.change_name)
async def save_new_name(message: Message, state: FSMContext):
    new_name = message.text

    await partial_update_user(data={'first_name': new_name}, user_id=message.chat.id)

    await message.answer(
        text = _("Name updated successfully ✅️"),
        reply_markup=await user_settings_keyboard()
    )

    await state.set_state(OrderState.order_type)



@router.message(F.text.in_(['🏙 Change city', "🏙 Shaharni o'zgartirish"]))
async def change_city(message: Message, state: FSMContext):
    cities = await get_all_cities()
    text = _("Please select the city")
    await message.answer(
        text,
        reply_markup=await default_keyboard_builder(
            message=message, keyboards=cities, column_name='name'
        )
    )
    await state.set_state(UpdateState.change_city)


@router.message(UpdateState.change_city)
async def update_city(message: Message, state: FSMContext):
    city = await get_city(city_name=message.text)

    await partial_update_user(data={'city_id': city.id}, user_id=message.chat.id)

    await message.answer(
        _("City successfully updated ✅️"),
        reply_markup=await user_settings_keyboard()
    )
    await state.set_state(OrderState.order_type)


@router.message(F.text.in_(['🇬🇧 Change language', "🇺🇿 Tilni o‘zgartirish"]))
async def settings_change_language(message: Message, state: FSMContext):
    text = _("🌐 Please select your language:")
    await message.answer(
        text,
        reply_markup=await get_language_keyboard()
    )
    await state.set_state(UpdateState.change_lang)



@router.message(F.text.in_(['✍️ Leave a feedback', '✍️ Fikr bildirish']))
async def feedback_button_handler(message: Message, state: FSMContext):
    text = _("✅ Les Ailes Service control.")
    await message.answer(text=text, reply_markup=await get_rating_keyboard())


@router.callback_query(
    F.data.startswith("product_") |
    F.data.startswith("package_") |
    F.data.startswith("delivery_")
)
async def rating_handler(callback: CallbackQuery):
    category, rating = callback.data.split("_")
    messages = {
        "product": _("You selected product rating:"),
        "package": _("You selected package rating:"),
        "delivery": _("You selected delivery rating:"),
    }

    await callback.message.answer(f"{messages[category]} {rating}")
    await callback.answer()


@router.message(F.text.in_(['📱Change number', "📱Raqamni o'zgartirish"]))
async def update_number_handler(message: Message, state: FSMContext):
    text = _("Please enter your new phone number:")
    await message.answer(text=text, reply_markup=phone_number)
    await state.set_state(UpdateState.change_phone)


@router.message(UpdateState.change_phone)
async def save_new_number(message: Message, state: FSMContext):
    if message.contact:
        new_number = message.contact.phone_number

    elif message.text:
        new_number = message.text.strip()
    else:
        text = _("Please send your phone number as text or via the 'Share Phone Number' button.")
        await message.answer(text=text)
        return


    cleaned = new_number.replace("+", "")
    if not cleaned.isdigit():
        text = _("Please enter a valid phone number (example: +998901234567).")
        await message.answer(text=text)
        return

    if len(cleaned) != 12:
        text = _("Phone number must contain 12 digits (example: +998901234567)")
        await message.answer(text=text)
        return

    await partial_update_user(
        data={'phone_number': new_number},
        user_id=message.chat.id
    )

    await message.answer(
        _("Phone number updated successfully ✅️"),
        reply_markup=await user_settings_keyboard()
    )

    await state.set_state(OrderState.order_type)
