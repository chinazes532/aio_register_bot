from aiogram import F, Router
from aiogram.types import Message

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb

from app.filters.admin_filter import AdminProtect

from app.database import insert_user

echo = Router()


@echo.message(F.text)
async def start_command(message: Message):
    admin = AdminProtect()
    if not await admin(message):  # Добавляем await здесь
        await message.answer(f'<b>Социальная скейт-школа приветствует Вас на регистрации в нашем боте!</b>',
                             parse_mode='HTML')
        await message.answer("<b>Выберите мероприятие:</b>",
                             parse_mode='HTML',
                             reply_markup=await bkb.events_cb())
        await insert_user(message.from_user.id, message.from_user.username)
    else:
        await message.answer(f'<b>Социальная скейт-школа приветствует Вас на регистрации в нашем боте!</b>',
                             parse_mode='HTML')
        await message.answer("<b>Выберите мероприятие:</b>",
                             parse_mode='HTML',
                             reply_markup=await bkb.events_cb())
        await insert_user(message.from_user.id, message.from_user.username)
        await message.answer(f"Вы успешно авторизовались как администратор!",
                             reply_markup=rkb.admin_menu)