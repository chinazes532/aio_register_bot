from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.states import AddEvent

from app.database import (insert_event, get_event_id,
                          get_all_users)

from app.functions.send_new_event import send_new_event


event = Router()


@event.callback_query(F.data == "create_event")
async def create_event(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer("<b>Введите название мероприятия:</b>",
                                  parse_mode='HTML',
                                  reply_markup=ikb.admin_cancel)

    await state.set_state(AddEvent.name)


@event.message(AddEvent.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("<b>Введите описание мероприятия:</b>",
                         parse_mode='HTML',
                         reply_markup=ikb.admin_cancel)

    await state.set_state(AddEvent.description)


@event.message(AddEvent.description)
async def description(message: Message, state: FSMContext):
    if len(message.text) < 1000:
        await state.update_data(description=message.html_text)
        await message.answer("<b>Введите количество участников на мероприятии:</b>",
                             parse_mode='HTML',
                             reply_markup=ikb.admin_cancel)

        await state.set_state(AddEvent.users_count)
    else:
        await message.answer("<b>Описание мероприятия должно содержать не более 1000 символов\n"
                             "Повторите попытку</b>",
                             parse_mode='HTML',
                             reply_markup=ikb.admin_cancel)


@event.message(AddEvent.users_count)
async def users_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(users_count=message.text)
        await message.answer("<b>Отправьте фото для мероприятия:</b>",
                             parse_mode='HTML',
                             reply_markup=ikb.admin_cancel)

        await state.set_state(AddEvent.photo)
    else:
        await message.answer("<b>Количество участников должно быть числом\n"
                             "Повторите попытку</b>",
                             parse_mode='HTML',
                             reply_markup=ikb.admin_cancel)


@event.message(AddEvent.photo)
async def photo(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(photo=message.photo[-1].file_id)
        await message.answer("<b>Отправьте файл для мероприятия, если файл отсутствует, то воспользуйтесь клавиатурой ниже:</b>",
                             parse_mode='HTML',
                             reply_markup=ikb.admin_send_file)
        await state.set_state(AddEvent.document)
    else:
        await message.answer("<b>Отправьте фото для мероприятия:</b>",
                             parse_mode='HTML',
                             reply_markup=ikb.admin_cancel)


@event.message(AddEvent.document)
async def photo(message: Message, state: FSMContext):
    if message.document:
        await state.update_data(document=message.document.file_id)
        data = await state.get_data()
        name = data.get("name")
        description = data.get("description")
        users_count = data.get("users_count")
        photo = data.get("photo")
        document = data.get("document")

        await insert_event(name, description, users_count, photo, document)
        event_id = await get_event_id(name, description, users_count, photo, document)

        await message.answer_photo(photo=photo,
                                   caption=f"<b>{name}</b>\n\n"
                                           f"{description}\n\n"
                                           f"Количество участников: {users_count} (видно только Вам)\n\n",
                                   parse_mode='HTML')
        await message.answer_document(document=document,
                                      caption=f"<b>Документ был успешно загружен!</b>\n\n",
                                      parse_mode='HTML')
        await message.answer(f"<b>Вы успешно создали мероприятие!</b>\n",
                             parse_mode='HTML',
                             reply_markup=ikb.admin_back_to_menu)

        await send_new_event(message.bot, photo, name, description, event_id)

        await state.clear()
    else:
        await message.answer("<b>Отправьте файл для мероприятия:</b>",
                             parse_mode='HTML',
                             reply_markup=ikb.admin_cancel)


@event.callback_query(AddEvent.document, F.data == "file_no")
async def file_no(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.update_data(document=None)
    data = await state.get_data()
    name = data.get("name")
    description = data.get("description")
    users_count = data.get("users_count")
    photo = data.get("photo")
    document = data.get("document")

    await insert_event(name, description, users_count, photo, document)
    event_id = await get_event_id(name, description, users_count, photo, document)

    await callback.message.answer_photo(photo=photo,
                               caption=f"<b>{name}</b>\n\n"
                                       f"{description}\n\n"
                                       f"Количество участников: {users_count} (видно только Вам)\n\n",
                               parse_mode='HTML')
    await callback.message.answer(f"<b>Вы успешно создали мероприятие!</b>\n",
                         parse_mode='HTML',
                         reply_markup=ikb.admin_back_to_menu)

    await send_new_event(callback.bot, photo, name, description, event_id)

    await state.clear()
