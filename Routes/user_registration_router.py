from typing import Any, Dict
from aiogram.filters import CommandStart, Command
from StatesGroup.Registration import Registration
from StatesGroup.Driver import Driver
from StatesGroup.Passenger import Passenger
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


registration_router = Router()

async def request_contact(message: Message):
    
    keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="share contact", request_contact = True),
                ]
            ],
            resize_keyboard=True,
        
        )

    await message.answer("share your contact by clicking the button.", reply_markup=keyboard)


async def register_user(message, user_data):

    await register_to_db(user_data)
    await message.answer('You Have been sucessfully registered' , reply_markup=ReplyKeyboardRemove())


@registration_router.message(Command("Unregister"))
@registration_router.message(F.text.casefold() == "unregister")
async def unregister_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to register
    """
    registered = await check_user_exists(message.from_user.id)
    if not registered:
        await message.answer("you are Not registered")
        return 
    
    await unregister_user(message.from_user.id)
    await message.reply('sucessfully Unregistered')

@registration_router.message(Command("register"))
@registration_router.message(F.text.casefold() == "register")
async def registration_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to register
    """
    registered = await check_user_exists(message.from_user.id)
    if registered:
        await message.answer("you are already registered", reply_markup=ReplyKeyboardRemove())
        return 
    
    await state.set_state(Registration.name)
    await message.answer(
        "please provide your full name?",
        reply_markup=ReplyKeyboardRemove(),
    )

@registration_router.message(Registration.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.update_data(id = message.from_user.id)
    await state.set_state(Registration.phone_number)
    await request_contact(message)

@registration_router.message(Registration.phone_number)
async def share_contact_handler(message: Contact , state: FSMContext) -> None:

    user_phone_number =  message.contact.phone_number
    await state.update_data(user_phone_number = user_phone_number)
    await state.set_state(Registration.role)
    role = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Driver"),
                    KeyboardButton(text ="Passenger")
                ]
            ],
            resize_keyboard=True,
        
        )
    await message.answer('What is your role' , reply_markup=role)

@registration_router.message(Registration.role)
async def role(message: Message , state: FSMContext) -> None:

    role = message.text
    await state.update_data(role = role)
    data = await state.get_data()
    await state.clear()
    await register_user(message, data)
    await state.set_state(Driver.dashboard if data.get('role').lower() == 'driver' else Passenger.dashboard)









    
