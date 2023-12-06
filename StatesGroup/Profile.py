from aiogram.fsm.state import State, StatesGroup

class Profile(StatesGroup):
    name = State()
    phone_number = State()
    