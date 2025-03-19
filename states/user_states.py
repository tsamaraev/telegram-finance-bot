from aiogram.fsm.state import State, StatesGroup


class RegisterStates(StatesGroup):
    username = State()
    currency = State()
    reminder_time = State()
