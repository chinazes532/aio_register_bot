from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

import app.keyboards.reply as rkb
import app.keyboards.builder as bkb
import app.keyboards.inline as ikb

from app.filters.admin_filter import AdminProtect

from app.database import (get_event, insert_register,
                          get_register_id, get_accepted_count)

from app.states import Register

from config import ADMINS

from app.functions.send_admins import send_admins

register = Router()


@register.callback_query(F.data.startswith("register_"))
async def register_callback(callback: CallbackQuery, state: FSMContext):
    event_id = int(callback.data.split("_")[1])
    event = await get_event(event_id)
    accepted_count = await get_accepted_count(event_id)
    await state.update_data(event_id=event_id)

    if accepted_count >= event[3]:
        await callback.answer("❗️Регистрация закрыта❗️",
                              show_alert=True)
    else:
        await callback.message.delete()
        await callback.message.answer("<b>Для регистрации введите ваше ФИО</b>\n\n",
                                     parse_mode='HTML',
                                     reply_markup=ikb.user_cancel)

        await state.set_state(Register.full_name)


@register.message(Register.full_name)
async def full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("<b>Укажите вашу дату рождения в формате: <code>дд.мм.гггг</code></b>\n\n",
                         parse_mode='HTML',
                         reply_markup=ikb.user_cancel)

    await state.set_state(Register.date_age)


@register.message(Register.date_age)
async def date_age(message: Message, state: FSMContext):
    date_input = message.text

    if date_input.count(".") == 2 and len(date_input) == 10 and date_input[2] == "." and date_input[5] == ".":
        await state.update_data(date_age=date_input)
        await message.answer("<b>Расскажите про ваш стаж катания.\n"
                             "Есть ли у Вас опыт катания, пробовали ли Вы стоять на скейтборде?</b>",
                             parse_mode='HTML',
                             reply_markup=ikb.user_cancel)

        await state.set_state(Register.rider_exp)
    else:
        await message.answer("<b>Неправильный формат даты. Попробуйте ещё раз.</b>\n\n",
                             parse_mode='HTML',
                             reply_markup=ikb.user_cancel)


@register.message(Register.rider_exp)
async def rider_exp(message: Message, state: FSMContext):
    if len(message.text) > 10:
        await state.update_data(rider_exp=message.text)

        await message.answer("<b>Есть ли у Вас свой скейтборд?</b>",
                             parse_mode='HTML',
                             reply_markup=ikb.skate)

        await state.set_state(Register.skate)
    else:
        await message.reply("<b>Расскажите про ваш стаж катания более подробно:</b>",
                            reply_markup=ikb.user_cancel,
                            parse_mode='HTML')


@register.callback_query(Register.skate)
async def skate_callback(callback: CallbackQuery, state: FSMContext):
    if callback.data == "skate_yes":
        await state.update_data(skate="Да")
    elif callback.data == "skate_no":
        await state.update_data(skate="Нет")

    await callback.answer()
    await callback.message.answer("<b>Есть ли у Вас шлем?</b>",
                                  parse_mode='HTML',
                                  reply_markup=ikb.helmet)

    await state.set_state(Register.helmet)


@register.callback_query(Register.helmet)
async def helmet_callback(callback: CallbackQuery, state: FSMContext):
    if callback.data == "helmet_yes":
        await state.update_data(helmet="Да")
    elif callback.data == "helmet_no":
        await state.update_data(helmet="Нет")

    await callback.answer()
    await callback.message.answer("<b>Есть ли у Вас своя защита?</b>",
                                  parse_mode='HTML',
                                  reply_markup=ikb.defender)

    await state.set_state(Register.defender)


@register.callback_query(Register.defender)
async def defender_callback(callback: CallbackQuery, state: FSMContext):
    if callback.data == "defender_yes":
        await state.update_data(defender="Да")
    elif callback.data == "defender_no":
        await state.update_data(defender="Нет")

    await callback.answer()
    await callback.message.answer("<b>Укажите ФИО родителя:</b>",
                                  parse_mode='HTML',
                                  reply_markup=ikb.user_cancel)

    await state.set_state(Register.parents_name)


@register.message(Register.parents_name)
async def parents_name(message: Message, state: FSMContext):
    await state.update_data(parents_name=message.text)
    await message.answer("<b>Укажите контактные данные родителя:</b>\n\n",
                         parse_mode='HTML',
                         reply_markup=ikb.user_cancel)

    await state.set_state(Register.parents_contact)


@register.message(Register.parents_contact)
async def parents_contact(message: Message, state: FSMContext):
    await state.update_data(parents_contact=message.text)
    await message.answer("<b>Укажите вашу электронную почту:</b>\n\n",
                         parse_mode='HTML',
                         reply_markup=ikb.user_cancel)
    await state.set_state(Register.email)


@register.message(Register.email)
async def parents_contact(message: Message, state: FSMContext, bot: Bot):
    if '@' in message.text:
        user_id = message.from_user.id
        await state.update_data(email=message.text)
        data = await state.get_data()
        full_name = data.get("full_name")
        date_age = data.get("date_age")
        rider_exp = data.get("rider_exp")
        skate = data.get("skate")
        helmet = data.get("helmet")
        defender = data.get("defender")
        parents_name = data.get("parents_name")
        parents_contact = data.get("parents_contact")
        event_id = data.get("event_id")
        email = data.get("email")

        event = await get_event(event_id)
        accepted_count = await get_accepted_count(event_id)
        await insert_register(full_name, date_age, rider_exp, skate, helmet, defender, parents_name, parents_contact, event_id, email)
        register_id = await get_register_id(full_name, date_age, rider_exp, skate, helmet, defender, parents_name, parents_contact, event_id, email)

        if accepted_count >= event[3]:
            await message.answer("<b>Регистрация закрыта!</b>", # <- обсудить текст сообщения с сашей
                                          parse_mode='HTML',
                                          reply_markup=ikb.user_back)
        else:
            await message.answer(f"Вы успешно зарегистрировались на мероприятие <b>{event[1]}</b>!\nВаша регистрация находится на модерации, ожидайте обратной связи!",
                                 parse_mode='HTML',
                                 reply_markup=ikb.user_back_to_menu)

            if event[5]:
                await message.answer_document(document=f"{event[5]}",
                                              caption="<b>Скачайте документ , заполните и принесите на тренировку</b>",
                                              reply_markup=ikb.user_back_to_menu,
                                              parse_mode='HTML')

            await send_admins(message.bot, full_name, date_age, rider_exp, skate, helmet, defender, parents_name, parents_contact, event_id, register_id, user_id, email)

        await state.clear()
    else:
        data = await state.get_data()
        event_id = data.get("event_id")
        event = await get_event(event_id)
        accepted_count = await get_accepted_count(event_id)
        if accepted_count >= event[3]:
            await message.answer("<b>Регистрация закрыта!</b>", # <- обсудить текст сообщения с сашей
                                          parse_mode='HTML',
                                          reply_markup=ikb.user_back)
        else:
            await message.answer("<b>Вы ввели некорректный адрес электронной почты, попробуйте еще раз!</b>",
                                 parse_mode='HTML',
                                 reply_markup=ikb.user_cancel)