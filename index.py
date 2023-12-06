import logging
import asyncio
import sys
from typing import Any, Dict
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from Routes.user_registration_router import registration_router
from Routes.start_router import start_router
from Routes.login_router import login_router
from Routes.passenger_router import passenger_router
from Routes.driver_router import driver_router
from Call_back_data.AcceptRide_callback import AcceptRide
from Repositories.ride_booking_db import accept_ride_request
from Routes.profile_management import profile_router
from dotenv import load_dotenv
import os
from aiogram.types.callback_query import CallbackQuery

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)

load_dotenv()

TOKEN = os.getenv('TOKEN')




router = Router()

router.include_router(start_router)
router.include_router(registration_router)
router.include_router(login_router)
router.include_router(passenger_router)
router.include_router(driver_router)
router.include_router(profile_router)

bot = Bot(token= TOKEN, parse_mode=ParseMode.HTML)

actions = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="View available rides"),
                    KeyboardButton(text="see my reviews"),
                ]
            ],
            resize_keyboard=True,
        
        )
@driver_router.callback_query(AcceptRide.filter())
async def accept_ride_callback_handler(query: CallbackQuery, callback_data:AcceptRide, state: FSMContext) -> None:
    ride_id = callback_data.ride_id
    user_id = callback_data.user_id
    user_data = await state.get_data()
    driver_id = user_data.get('driver_id')
    user_name = callback_data.user_name

    await bot.send_message(user_id, f"Your ride request has been accepted by {user_name}")
    await accept_ride_request(ride_id, driver_id)
    await query.answer(text="Ride accepted", reply_markup=actions)

async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

