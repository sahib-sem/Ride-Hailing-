from typing import Any, Dict
from aiogram.filters import CommandStart
from aiogram import Router, F, html
from StatesGroup.Driver import Driver
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Contact
)


driver_router = Router()

@driver_router.message(Driver.dashboard)

async def driver_dashboard(message: Message, state: FSMContext) -> None:

    print('driver dashboard')
    await message.answer(
        "welcome Driver"
        )



