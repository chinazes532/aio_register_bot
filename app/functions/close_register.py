from aiogram import Bot
from config import ADMINS
from app.database import get_event, get_accepted_count


async def close_register(event_id, bot: Bot):
    count = await get_accepted_count(event_id)
    event = await get_event(event_id)
    if count == event[3]:
        for admin in ADMINS:
            try:
                await bot.send_message(chat_id=admin,
                                       text=f"Регистрация на мероприятие <b>{event[1]}</b> закрыта!",
                                       parse_mode='HTML')
            except Exception as e:
                if str(e) == 'Telegram server says - Bad Request: chat not found':
                    continue
                else:
                    await bot.send_message(chat_id=7339750868,
                                           text=f"{e}")
    else:
        pass