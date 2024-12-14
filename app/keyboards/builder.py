from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database import get_all_events, get_all_rejected


async def send_event(event_id):
    kb = InlineKeyboardBuilder()

    kb.add(InlineKeyboardButton(text="Зарегистрироваться", callback_data=f"register_{event_id}"))

    return kb.as_markup()


async def register(event_id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text="Зарегистрироваться", callback_data=f"register_{event_id}"))
    kb.row(InlineKeyboardButton(text="Назад ↩️", callback_data="user_cancel"))

    return kb.as_markup()


async def events_cb():
    kb = InlineKeyboardBuilder()

    events = await get_all_events()
    for event in events:
        kb.row(InlineKeyboardButton(text=event[1], callback_data=f"event_{event[0]}"))

    return kb.as_markup()


async def admin_events_cb():
    kb = InlineKeyboardBuilder()

    events = await get_all_events()
    for event in events:
        kb.row(InlineKeyboardButton(text=event[1], callback_data=f"adminevent_{event[0]}"))

    kb.row(InlineKeyboardButton(text="Назад ↩️", callback_data="admin_cancel"))

    return kb.as_markup()


async def second_admin_events_cb():
    kb = InlineKeyboardBuilder()

    events = await get_all_events()
    for event in events:
        kb.row(InlineKeyboardButton(text=event[1], callback_data=f"secondadminevent_{event[0]}"))

    kb.row(InlineKeyboardButton(text="Назад ↩️", callback_data="admin_cancel"))

    return kb.as_markup()


async def check_register(user_id, register_id, event_id):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="✅Принять", callback_data=f"accept_register_{register_id}_{user_id}_{event_id}"))
    kb.add(InlineKeyboardButton(text="❌Отклонить", callback_data=f"decline_register_{register_id}_{user_id}_{event_id}"))
    return kb.as_markup()


async def rejects_cb():
    kb = InlineKeyboardBuilder()
    rejects = await get_all_rejected()
    for reject in rejects:
        kb.row(InlineKeyboardButton(text=reject[1], callback_data=f"reject_{reject[0]}"))
    kb.row(InlineKeyboardButton(text="Назад ↩️", callback_data="admin_cancel"))
    return kb.as_markup()


async def edit_event(event_id):
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_{event_id}"))
    kb.row(InlineKeyboardButton(text="✏️ Редактировать название", callback_data=f"name_{event_id}"))
    kb.row(InlineKeyboardButton(text="📜 Редактировать описание", callback_data=f"description_{event_id}"))
    kb.row(InlineKeyboardButton(text="🖼️ Редактировать фото", callback_data=f"photo_{event_id}"))
    kb.row(InlineKeyboardButton(text="🔢 Редактировать ограничение", callback_data=f"users_count_{event_id}"))
    kb.row(InlineKeyboardButton(text="Назад ↩️", callback_data="admin_cancel"))
    return kb.as_markup()

