from aiogram.filters.callback_data import CallbackData

class AcceptRide(CallbackData, prefix="my"):
    ride_id: int
    user_id: int
    user_location: str
    user_name: str

    