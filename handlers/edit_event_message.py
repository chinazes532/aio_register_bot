from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.states import AddEvent

from app.database import (delete_register, delete_accepted,
                          get_event, delete_event, update_event_name, update_event_description,
                          update_event_users_count, update_event_photo)


edit = Router()


@edit.callback_query(F.data == "edit_event")
async def edit_event(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer("<b>Выберите мероприятие:</b>",
                                  reply_markup=await bkb.admin_events_cb(),
                                  parse_mode='HTML')


@edit.callback_query(F.data.startswith("adminevent_"))
async def edit_event(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    event_id = int(callback.data.split("_")[1])
    event = await get_event(event_id)

    await callback.message.answer_photo(photo=event[4],
                                        caption=f"<b>{event[1]}</b>\n\n"
                                                f"{event[2]}\n\n"
                                                f"<b>Максимальное количество участников:{event[3]}\n\n"
                                                f"Выберите действие:</b>",
                                        parse_mode='HTML',
                                        reply_markup=await bkb.edit_event(event_id))


@edit.callback_query(F.data.startswith("delete_"))
async def delete_event_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    event_id = int(callback.data.split("_")[1])

    await delete_event(event_id)
    await delete_register(event_id)
    await delete_accepted(event_id)

    await callback.message.answer("<b>Мероприятие удалено</b>",
                                  reply_markup=await bkb.admin_events_cb(),
                                  parse_mode='HTML')


@edit.callback_query(F.data.startswith("name_"))
async def edit_event_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    event_id = int(callback.data.split("_")[1])

    await state.update_data(event_id=event_id)
    await callback.message.answer("<b>Новое название мероприятия:</b>",
                                  reply_markup=ikb.admin_cancel,
                                  parse_mode='HTML')
    await state.set_state(AddEvent.new_name)


@edit.message(AddEvent.new_name)
async def edit_event_new_name(message: Message, state: FSMContext):
    data = await state.get_data()
    event_id = data.get("event_id")

    event = await get_event(event_id)
    await update_event_name(event_id, message.text)

    await message.answer_photo(photo=event[4],
                               caption=f"<b><u>{message.text}</u></b>\n\n"
                                       f"{event[2]}\n\n"
                                       f"<b>Максимальное количество участников:{event[3]}</b>\n\n",
                               parse_mode='HTML')

    await message.answer("<b>Название изменено\n"
                         "Выберите действие:</b>",
                         reply_markup=await bkb.edit_event(event_id),
                         parse_mode='HTML')
    await state.clear()


@edit.callback_query(F.data.startswith("description_"))
async def edit_event_description(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    event_id = int(callback.data.split("_")[1])

    await state.update_data(event_id=event_id)
    await callback.message.answer("<b>Новое описание мероприятия:</b>",
                                  reply_markup=ikb.admin_cancel,
                                  parse_mode='HTML')
    await state.set_state(AddEvent.new_description)


@edit.message(AddEvent.new_description)
async def edit_event_new_description(message: Message, state: FSMContext):
    if len(message.text) < 1000:
        data = await state.get_data()
        event_id = data.get("event_id")

        event = await get_event(event_id)
        await update_event_description(event_id, message.text)

        await message.answer_photo(photo=event[4],
                                   caption=f"<b>{event[1]}</b>\n\n"
                                           f"<u>{message.text}</u>\n\n"
                                           f"<b>Максимальное количество участников:{event[3]}</b>\n\n",
                                   parse_mode='HTML')

        await message.answer("<b>Описание изменено\n"
                             "Выберите действие:</b>",
                             reply_markup=await bkb.edit_event(event_id),
                             parse_mode='HTML')
        await state.clear()
    else:
        await message.answer("<b>Максимальная длина описания - 1000 символов\n"
                             "Попробуйте ещё раз</b>",
                             reply_markup=ikb.admin_cancel,
                             parse_mode='HTML')


@edit.callback_query(F.data.startswith("users_count_"))
async def edit_event_users_count(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    event_id = int(callback.data.split("_")[2])

    await state.update_data(event_id=event_id)
    await callback.message.answer("<b>Новое количество мест:</b>",
                                  reply_markup=ikb.admin_cancel,
                                  parse_mode='HTML')

    await state.set_state(AddEvent.new_users_count)


@edit.message(AddEvent.new_users_count)
async def edit_event_new_users_count(message: Message, state: FSMContext):
    if message.text.isdigit():
        data = await state.get_data()
        event_id = data.get("event_id")

        event = await get_event(event_id)
        await update_event_users_count(event_id, message.text)

        await message.answer_photo(photo=event[4],
                                   caption=f"<b>{event[1]}</b>\n\n"
                                           f"{event[2]}\n\n"
                                           f"<b>Максимальное количество участников: <u>{message.text}</u></b>\n\n",
                                   parse_mode='HTML')

        await message.answer("<b>Количество мест изменено\n"
                             "Выберите действие:</b>",
                             reply_markup=await bkb.edit_event(event_id),
                             parse_mode='HTML')
        await state.clear()
    else:
        await message.answer("<b>Только цифры\n"
                             "Попробуйте ещё раз</b>",
                             reply_markup=ikb.admin_cancel,
                             parse_mode='HTML')


@edit.callback_query(F.data.startswith("photo_"))
async def edit_event_photo(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    event_id = int(callback.data.split("_")[1])

    await state.update_data(event_id=event_id)
    await callback.message.answer("<b>Новое фото мероприятия:</b>",
                                  reply_markup=ikb.admin_cancel,
                                  parse_mode='HTML')

    await state.set_state(AddEvent.new_photo)


@edit.message(AddEvent.new_photo)
async def edit_event_new_photo(message: Message, state: FSMContext):
    if message.photo:
        data = await state.get_data()
        event_id = data.get("event_id")
        event = await get_event(event_id)

        await update_event_photo(event_id, message.photo[-1].file_id)

        await message.answer_photo(photo=message.photo[-1].file_id,
                                   caption=f"<b>{event[1]}</b>\n\n"
                                           f"{event[2]}\n\n"
                                           f"<b>Максимальное количество участников: {event[3]}</b>\n\n",
                                   parse_mode='HTML')

        await message.answer("<b>Фото изменено\n"
                             "Выберите действие:</b>",
                             reply_markup=await bkb.edit_event(event_id),
                             parse_mode='HTML')
        await state.clear()
    else:
        await message.answer("<b>Только фото\n"
                             "Попробуйте ещё раз</b>",
                             reply_markup=ikb.admin_cancel,
                             parse_mode='HTML')