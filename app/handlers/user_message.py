from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.filters.admin_filter import AdminProtect

from app.database import insert_user, get_event

user = Router()


@user.message(CommandStart())
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


@user.callback_query(F.data.startswith("event_"))
async def event_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    event_id = int(callback.data.split("_")[1])
    event = await get_event(event_id)

    await callback.message.answer_photo(photo=event[4],
                                       caption=f"<b>{event[1]}</b>\n\n"
                                               f"{event[2]}\n\n",
                                        parse_mode='HTML',
                                        reply_markup=await bkb.register(event_id))


