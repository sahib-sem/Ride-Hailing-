from typing import Any, Dict
from aiogram.filters import CommandStart
from aiogram import Router, F, html
from StatesGroup.Driver import Driver
from Call_back_data.AcceptRide_callback import AcceptRide
import logging
from Repositories.ride_booking_db import get_ride_requests, accept_ride_request
from Repositories.user_db import get_name

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)


driver_router = Router()

actions = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="View available rides"),
                    KeyboardButton(text="see my reviews"),
                ]
            ],
            resize_keyboard=True,
        
        )

@driver_router.message(Driver.dashboard)

async def driver_dashboard(message: Message, state: FSMContext) -> None:

    actions = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="View available rides"),
                    KeyboardButton(text="see my reviews"),
                ]
            ],
            resize_keyboard=True,
        
        )
    
    await state.clear()
    await message.answer(
        "welcome Driver", reply_markup=actions
        
        )
    
@driver_router.message(F.text.casefold() == "view available rides")
async def view_available_rides(message: Message, state: FSMContext) -> None:
    
    available_rides = await get_ride_requests()
    await state.update_data(driver_id = message.from_user.id)
    if not available_rides:
        await message.answer('No available rides', reply_markup=actions)
        return
    
    
    for ride in available_rides:

        user_name = await get_name(ride[1])
        ride_action = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Accept", callback_data= AcceptRide(ride_id=ride[0], user_id=ride[1], user_location=ride[2], user_name=user_name).pack()),

            ]
        ]
    )

        await message.answer( f"Ride ID: {ride[0]}\nUser ID: {ride[1]}\nUser Location: {ride[2]}\nAccepted Status: {ride[3]}\nDriver ID: {ride[4]}", reply_markup=ride_action)




