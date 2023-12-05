import logging
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher, Router, html
from aiogram.enums import ParseMode
from Routes.Form_router import form_router
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application


from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)


TOKEN = '6799461460:AAHLQnh5Fc-cr2J4JmhsZ1C0UfGtNRu3Ais'

WEB_SERVER_HOST = "127.0.0.1"
WEB_SERVER_PORT = 8080

WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_SECRET = "my-secret"
BASE_WEBHOOK_URL = "https://e6c5-196-189-150-186.ngrok.io"


router = Router()

router.include_router(form_router)

async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)

def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_startup)
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
