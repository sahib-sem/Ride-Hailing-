import logging
import asyncio
import sys
from aiogram import Bot, Dispatcher, Router, html
from aiogram.enums import ParseMode
from Routes.user_registration_router import registration_router
from Routes.start_router import start_router
from dotenv import load_dotenv
import os

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)

load_dotenv()

TOKEN = os.getenv('TOKEN')




router = Router()

router.include_router(start_router)
router.include_router(registration_router)

bot = Bot(token= TOKEN, parse_mode=ParseMode.HTML)

async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())