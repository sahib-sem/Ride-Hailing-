from typing import Any, Dict
from aiogram.filters import CommandStart, Command
from StatesGroup.Registration import Registration
from aiogram import Router, F, html
import logging
from Repositories.user_db import check_user_exists, register_user as register_to_db, unregister_user

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
    """
    if user is not registered, ask user to register
    else login user

    """
    