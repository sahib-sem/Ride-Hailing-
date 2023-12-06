from aiogram.filters import Command
from aiogram import Router, F
from StatesGroup.Profile import Profile
from StatesGroup.Driver import Driver
from StatesGroup.Passenger import Passenger
from Repositories.user_db import  check_user_exists, update_user_name, update_user_phone_number, get_user_role

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Contact
)


profile_router = Router()

@profile_router.message(Command("profile management"))
@profile_router.message(F.text.casefold() == "profile management")
async def profile_management_handler(message: Message, state: FSMContext) -> None:
    
    registered = await check_user_exists(message.from_user.id)
    if not registered:
        await message.answer("you are Not registered")
        return
    
    edit = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Edit name"),
                    KeyboardButton(text="Edit phone number", request_contact= True),
                ]
            ],
            resize_keyboard=True,
        
        )

    await message.answer("What would you like to edit?", reply_markup=edit)

@profile_router.message(F.text.casefold() == "edit name")
async def edit_name_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Please enter your new name", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Profile.name)

@profile_router.message(F.text.casefold() == "edit phone number")
async def edit_phone_number_handler(message: Contact, state: FSMContext) -> None:
    
    phone_number = message.contact.phone_number
    await state.clear()
    await update_user_phone_number(message.from_user.id, phone_number)

    role = await get_user_role(message.from_user.id)
    await state.set_state(Driver.dashboard if role == 'driver' else Passenger.dashboard)


@profile_router.message(Profile.name)
async def edit_name(message: Message, state: FSMContext) -> None:
    await update_user_name(message.from_user.id, message.text)
    await message.answer("Your name has been updated")
    await state.clear()

    role = await get_user_role(message.from_user.id)
    await state.set_state(Driver.dashboard if role == 'driver' else Passenger.dashboard)