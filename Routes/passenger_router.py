from aiogram import Router, F, html
from StatesGroup.Passenger import Passenger
from Repositories.ride_booking_db import save_ride_request, cancel_ride as cr

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Contact
)

actions = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Book a ride"),
                KeyboardButton(text="Cancel a ride"),
                KeyboardButton(text="View your rides"),
            ]
        ],
        resize_keyboard=True,
    
    )

passenger_router = Router()

@passenger_router.message(Passenger.dashboard)
async def passenger_dashboard(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "welcome Passenger", reply_markup=actions
        )


@passenger_router.message(F.text.casefold() == "book a ride")
async def book_ride(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    
    await state.update_data(user_id = user_id)
    await state.set_state(Passenger.BookRide)
    location = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="share location", request_location = True),
                ]
            ],
            resize_keyboard=True,

        )
    await message.answer(
        "share your location", reply_markup=location
        )

@passenger_router.message(F.text.casefold() == "cancel a ride")
async def cancel_ride(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    ride_id = user_data.get('ride_id')
    await cr(ride_id)
    await message.answer('Ride cancelled', reply_markup=actions)
    
@passenger_router.message(Passenger.BookRide)
async def book_ride(message: Message, state: FSMContext) -> None:
    
    user_location = f'{message.location.latitude},{message.location.longitude}'

    await state.update_data(user_location = user_location)
    user_data = await state.get_data()
    ride_id = await save_ride_request(user_data)
    await state.update_data(ride_id = ride_id)

    await message.answer('You will be notified when a driver accepts your request' , reply_markup=actions)
    
        
