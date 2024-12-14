from aiogram import Bot

from app.database import get_event
from config import ADMINS
import app.keyboards.builder as bkb


async def send_admins(bot: Bot, full_name, date_age, rider_exp, skate, helmet, defender, parents_name, parents_contact, event_id, register_id, user_id, email):
    event = await get_event(event_id)
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=admin,
                                   text=f"<b>Новая регистрация на {event[1]}</b>\n\n"
                                        f"<b>ФИО:</b> {full_name}\n"
                                        f"<b>Дата рождения:</b> {date_age}\n"
                                        f"<b>Стаж катания:</b> {rider_exp}\n"
                                        f"<b>Наличие скейта:</b> {skate}\n"
                                        f"<b>Наличие шлема:</b> {helmet}\n"
                                        f"<b>Наличие защиты:</b> {defender}\n"
                                        f"<b>ФИО родителя:</b> {parents_name}\n"
                                        f"<b>Контакты родителя:</b> {parents_contact}\n"
                                        f"<b>Электронная почта:</b> {email}\n",
                                   parse_mode='HTML',
                                   reply_markup=await bkb.check_register(user_id, event_id, register_id))

        except Exception as e:
            if str(e) == 'Telegram server says - Bad Request: chat not found':
                continue
            else:
                await bot.send_message(chat_id=7339750868,
                                       text=f"{e}")