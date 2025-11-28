from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from django.utils.translation import gettext as _

from bot.keyboards.default.order import get_takeaway_keyboards, get_delivery_keyboards
from bot.keyboards.inline.order import get_proceed_button
from bot.states.order import OrderState

router = Router()


@router.message(F.text.in_(['🗺 My addresses', '🗺 Mening manzillarim']))
async def address_handler(message: Message, state: FSMContext):
    # await state.set_state(OrderState.location)
    # await state.update_data(order_type="delivery")

    text = _("You do not have any saved addresses")
    await message.answer(text=text, reply_markup=await get_delivery_keyboards())


@router.message(F.text.in_(['🙋🏻‍♂️ Join to our team', "🙋🏻‍♂️ Jamoamizga qo'shiling"]))
async def vacancies_handler(message: Message, state: FSMContext):
    # await state.set_state(OrderState.location)
    # await state.update_data(order_type="delivery")

    text = _("Join our friendly team our friendly team! Click on the button below to fill out the questionnaire right here, without leaving Telegram.")
    await message.answer(text=text, reply_markup=await get_proceed_button(button_name=_("Proceed"), link="https://t.me/myexceptionns"))


@router.message(F.text.in_(['☎️ Contact', "☎️ Biz bilan aloqa"]))
async def vacancies_handler(message: Message, state: FSMContext):
    # await state.set_state(OrderState.location)
    # await state.update_data(order_type="delivery")

    text = _("Join our friendly team our friendly team! Click on the button below to fill out the questionnaire right here, without leaving Telegram.")
    await message.answer(text=text, reply_markup=await get_proceed_button(button_name=_("Proceed"), link="https://t.me/myexceptionns"))

