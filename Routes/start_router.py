from typing import Any, Dict
from aiogram.filters import CommandStart
from aiogram import Router, F, html
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Contact
)


start_router = Router()

@start_router.message(CommandStart())
async def command_start(message: Message) -> None:
    
    await message.answer(
        f"Welcome to Ride Hailing! \n Would you like to Register?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Register"),
                    KeyboardButton(text="Unregister"),
                    KeyboardButton(text="Login"),
                    KeyboardButton(text="Profile Management"),
                ]
            ],
            resize_keyboard=True,
        )
        )

