from aiogram.filters import Command
from StatesGroup.Driver import Driver
from StatesGroup.Passenger import Passenger
from aiogram import Router, F
from Repositories.user_db import get_user_role, check_user_exists

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Contact
)


login_router = Router()

@login_router.message(Command("login"))
@login_router.message(F.text.casefold() == "login")
async def login_handler(message: Message, state: FSMContext) -> None:
    
    registered = await check_user_exists(message.from_user.id)
    if not registered:
        await message.answer("you are Not registered")
        return
    role = await get_user_role(message.from_user.id)
    await state.clear()
    await state.set_state(Driver.dashboard if role.lower() == 'driver' else Passenger.dashboard)
    print(await state.get_state())
    dashboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="dashboard"),
                ]
            ],
            resize_keyboard=True,
        
        )
    await message.answer('press the button to go to your dashboard' , reply_markup=dashboard)

