from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from django.utils.translation import gettext as _

from bot.keyboards.default.order import get_takeaway_keyboards, get_delivery_keyboards
from bot.keyboards.default.user import get_user_main_keyboards
from bot.keyboards.inline.order import get_proceed_button
from bot.states.order import OrderState

router = Router()


@router.message(F.text.in_(['🏃‍♂️ Take away', '🏃‍♂️ Olib ketish']), OrderState.order_type)
async def take_away_handler(message: Message, state: FSMContext):
    await state.update_data(order_type='take_away')
    await state.set_state(OrderState.location)

    text = _("Where are you? Send your location and we determine the nearest branch to you")
    await message.answer(text=text, reply_markup=await get_takeaway_keyboards())


@router.message(
    F.text.in_(['📍Determine nearest branch', '📍 Eng yaqin filialni aniqlash']),
    OrderState.location
)
async def location_button_handler(message: Message, state: FSMContext):
    text = _("Please send your location using the button below")
    await message.answer(text=text)


@router.message(F.location, OrderState.location)
async def location_received_handler(message: Message, state: FSMContext):
    await state.update_data(
        longitude=message.location.longitude,
        latitude=message.location.latitude
    )
    await state.set_state(OrderState.category)

    text = _("Where to start?")
    await message.answer(text=text)
    # Echo back the location
    await message.answer_location(
        longitude=message.location.longitude,
        latitude=message.location.latitude
    )


@router.message(F.text.in_(["🌐 Order here",  "🌐 Bu yerdan buyurtma berish"]))
async def order_handler(message: Message, state: FSMContext):
        text = _("Order with your location - ") + "https://lesailes.uz/"
        await message.answer(text=text, reply_markup=await get_proceed_button(button_name=_("Proceed"), link="https://lesailes.uz/"))


@router.message(F.text.in_(["Select branch",  "Manzilni tanlang"]))
async def address_handler(message: Message, state: FSMContext):
        text = _("Here you can see all branches of Les Ailes")
        await message.answer(text=text)



@router.message(F.text.in_(['🚙 Delivery', '🚙 Yetkazib berish']), OrderState.order_type)
async def delivery_handler(message: Message, state: FSMContext):
    await state.set_state(OrderState.location)
    await state.update_data(order_type="delivery")

    text = _("Where to deliver? Send your location and we determine the nearest branch and delivery cost.")
    await message.answer(text=text, reply_markup=await get_delivery_keyboards())


@router.message(F.text.in_(['🔥 Promotions', '🔥 Aksiya va chegirmalar']))
async def promotions_handler(message: Message, state: FSMContext):
    # await state.set_state(OrderState.location)
    # await state.update_data(order_type="delivery")

    text = _("There is no promotions in your city")
    await message.answer(text=text)

