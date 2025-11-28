from aiogram.fsm.state import StatesGroup, State


class OrderState(StatesGroup):
    order_type = State()
    location = State()
    category = State()