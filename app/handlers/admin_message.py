from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.database import (get_event, insert_accepted,
                          get_register,
                          insert_rejected,
                          get_accepted, get_rejected,
                          get_rejected_count, save_to_excel)

from app.filters.admin_filter import AdminProtect

from app.states import Reject

from app.functions.close_register import close_register


admin = Router()


@admin.message(AdminProtect(), Command("admin"))
@admin.message(AdminProtect(), F.text == "Админ-панель 🛠️")
async def admin_panel(message: Message):
    await message.answer(f"Вы вошли в админ-панель!\n"
                         f"Выберите действие",
                         reply_markup=ikb.admin_panel)


@admin.callback_query(F.data.startswith("accept_register_"))
async def accept_register(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    await callback.message.delete()

    register_id = int(callback.data.split("_")[4])
    event_id = int(callback.data.split("_")[2])
    user_id = int(callback.data.split("_")[3])

    accepted = await get_accepted(register_id)
    rejected = await get_rejected(register_id)
    event = await get_event(event_id)
    register = await get_register(register_id)

    if accepted:
        await callback.message.answer("<b>Заявка уже принята!</b>", parse_mode='HTML')
    elif rejected:
        await callback.message.answer("<b>Заявка уже отклонена!</b>", parse_mode='HTML')
    else:
        await insert_accepted(register_id=register_id,
                              full_name=register[1],
                              date_age=register[2],
                              rider_exp=register[3],
                              skate=register[4],
                              helmet=register[5],
                              defender=register[6],
                              parents_name=register[7],
                              parents_contact=register[8],
                              email=register[10],
                              event_id=event_id)
        await bot.send_message(chat_id=user_id,
                               text=f"Ваша регистрация на мероприятие <b>{event[1]}</b> принята!\n"
                                    f"Ждем Вас!",
                               parse_mode='HTML')
        await callback.message.answer(f"Вы успешно приняли регистрацию!")
        await close_register(event_id, bot)


@admin.callback_query(F.data.startswith("decline_register_"))
async def decline_register(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()

    register_id = int(callback.data.split("_")[4])
    event_id = int(callback.data.split("_")[2])
    user_id = int(callback.data.split("_")[3])

    accepted = await get_accepted(register_id)
    rejected = await get_rejected(register_id)

    # Проверка на статус заявки
    if accepted:
        await callback.message.answer("<b>Заявка уже принята!</b>", parse_mode='HTML')
        await state.clear()
        return
    elif rejected:
        await callback.message.delete()
        await callback.message.answer("<b>Заявка уже отклонена!</b>", parse_mode='HTML')
        await state.clear()
        return

    await state.update_data(register_id=register_id)
    await state.update_data(event_id=event_id)
    await state.update_data(user_id=user_id)

    await callback.message.answer('<b>Напишите причину отклонения:</b>',
                                  reply_markup=ikb.admin_cancel,
                                  parse_mode='HTML')
    await state.set_state(Reject.reason)


@admin.message(Reject.reason)
async def reason(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(reason=message.text)
    data = await state.get_data()
    register_id = data.get("register_id")
    event_id = data.get("event_id")
    user_id = data.get("user_id")

    register = await get_register(register_id)
    event = await get_event(event_id)

    await bot.send_message(chat_id=user_id,
                           text=f"Ваша регистрация на мероприятие <b>{event[1]}</b> отклонена!\n"
                                f"Причина: <b><u>{message.text}</u></b>\n",
                           parse_mode='HTML')

    await insert_rejected(register_id=register_id,
                          full_name=register[1],
                          date_age=register[2],
                          rider_exp=register[3],
                          skate=register[4],
                          helmet=register[5],
                          defender=register[6],
                          parents_name=register[7],
                          parents_contact=register[8],
                          email=register[10],
                          event_id=event_id,
                          reason=message.text)
    await message.answer("<b>Вы успешно отклонили регистрацию!</b>",
                         parse_mode='HTML')

    await state.clear()


@admin.callback_query(F.data == "decline_list")
async def decline_list(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    count = await get_rejected_count()

    if count == 0:
        pass
    else:
        await callback.message.answer(f"Всего отклонено заявок: <b>{count}</b>\n"
                                      f"Вот список из всех заявок:",
                                      parse_mode='HTML',
                                      reply_markup=await bkb.rejects_cb())


@admin.callback_query(F.data.startswith("reject_"))
async def reject_list(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    reject_id = int(callback.data.split('_')[1])
    reject = await get_rejected(reject_id)
    await callback.message.answer(f'<b>Отклоненная заявка №{reject[0]}\n\n</b>'
                                  f'<b>ФИО:</b> {reject[1]}\n'
                                  f'<b>Дата рождения:</b> {reject[2]}\n'
                                  f'<b>Стаж катания:</b> {reject[3]}\n'
                                  f'<b>Наличие скейта:</b> {reject[4]}\n'
                                  f'<b>Наличие шлема:</b> {reject[5]}\n'
                                  f'<b>Наличие защиты:</b> {reject[6]}\n'
                                  f'<b>ФИО родителей:</b> {reject[7]}\n'
                                  f'<b>Контакты родителей:</b> {reject[8]}\n'
                                  f'<b>Электронная почта:</b> {reject[11]}\n'
                                  f'<b>Причина отклонения заявки:</b> {reject[10]}',
                                  reply_markup=ikb.admin_back,
                                  parse_mode='HTML')


@admin.callback_query(F.data == "records")
async def records(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer("<b>Выберите мероприятие:</b>",
                                  reply_markup=await bkb.second_admin_events_cb(),
                                  parse_mode='HTML')


@admin.callback_query(F.data.startswith("secondadminevent_"))
async def records(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    event_id = int(callback.data.split('_')[1])
    event = await get_event(event_id)

    # Используем await для получения пути к файлу
    file_path = await save_to_excel(event_id, event[1])

    # Убедитесь, что вы передаете путь к файлу
    input_file = FSInputFile(path=file_path)  # Здесь используем 'path' вместо 'filename'

    await callback.message.answer_document(document=input_file,
                                           caption=f"<b>{event[1]}</b>\n\n",
                                           reply_markup=ikb.admin_back,
                                           parse_mode='HTML')






