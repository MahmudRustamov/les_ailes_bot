from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    language = State()
    city = State()
    phone_number = State()


class UpdateState(StatesGroup):
    change_city = State()
    change_name = State()
    change_phone = State()
    change_lang = State()