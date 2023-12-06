
from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    name = State()
    phone_number = State()
    role = State()
    