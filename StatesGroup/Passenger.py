from aiogram.fsm.state import State, StatesGroup

class Passenger(StatesGroup):
    dashboard = State()
    BookRide = State()
    CancelRide = State()
    RideHistory = State()
    