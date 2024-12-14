import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from app.handlers.user_message import user
from app.handlers.admin_message import admin
from app.handlers.event_message import event
from app.handlers.cancel_message import cancel
from app.handlers.register_message import register
from app.handlers.edit_event_message import edit
from app.handlers.echo_message import echo

from app.database import create_db


async def main():
    print("Bot is starting...")

    await create_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user)
    dp.include_router(register)
    dp.include_router(admin)
    dp.include_router(edit)
    dp.include_router(event)
    dp.include_router(cancel)
    dp.include_router(echo)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")