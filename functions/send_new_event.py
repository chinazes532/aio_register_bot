from aiogram import Bot

from app.database import get_all_users

import app.keyboards.builder as bkb


async def send_new_event(bot: Bot, photo, name, description, event_id):
    users = await get_all_users()
    for user in users:
        try:
            await bot.send_photo(photo=photo,
                                 caption=f"<b>{name}</b>\n\n"
                                         f"{description}\n\n",
                                 parse_mode='HTML',
                                 chat_id=user[0],
                                 reply_markup=await bkb.send_event(event_id))
        except Exception as e:
            if str(e) == 'Forbidden: bot was blocked by the user':
                continue
            else:
                await bot.send_message(chat_id=7339750868,
                                       text=f"{e}")