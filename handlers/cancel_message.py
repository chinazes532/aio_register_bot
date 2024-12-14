from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb
from app.database import get_rejected_count

cancel = Router()


@cancel.callback_query(F.data == "admin_cancel")
async def admin_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer("<b>Вы вернулись в админ-панель</b>",
                                  parse_mode='HTML',
                                  reply_markup=ikb.admin_panel)

    await state.clear()


@cancel.callback_query(F.data == "user_cancel")
async def user_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer("<b>Выберите мероприятие:</b>",
                         parse_mode='HTML',
                         reply_markup=await bkb.events_cb())

    await state.clear()


@cancel.callback_query(F.data == "user_back_to_menu")
async def user_back_to_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.answer(f'<b>Социальная скейт-школа приветствует Вас на регистрации в нашем боте!</b>',
                         parse_mode='HTML')
    await callback.message.answer("<b>Выберите мероприятие:</b>",
                         parse_mode='HTML',
                         reply_markup=await bkb.events_cb())

    await state.clear()


@cancel.callback_query(F.data == "user_back")
async def user_back_to_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer("<b>Выберите мероприятие:</b>",
                         parse_mode='HTML',
                         reply_markup=await bkb.events_cb())

    await state.clear()


@cancel.callback_query(F.data == "admin_cancel")
async def admin_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer("<b>Вы вернулись в админ-панель</b>",
                                  parse_mode='HTML',
                                  reply_markup=ikb.admin_panel)

    await state.clear()


@cancel.callback_query(F.data == "admin_back_to_registration")
async def admin_back_to_registration(callback: CallbackQuery, state: FSMContext):
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

    await state.clear()