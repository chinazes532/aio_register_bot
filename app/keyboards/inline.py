from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Регистрации 📝", callback_data="records")],
        [InlineKeyboardButton(text="Создать мероприятие 🛹", callback_data="create_event")],
        [InlineKeyboardButton(text="Редактировать мероприятие ✏️", callback_data="edit_event")],
        [InlineKeyboardButton(text="Список отклонений 📋", callback_data="decline_list")]
    ]
)

admin_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отмена ❌", callback_data="admin_cancel")]
    ]
)

user_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отмена ❌", callback_data="user_cancel")]
    ]
)

user_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад ⬅️", callback_data="user_back")]
    ]
)

skate = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да ✅", callback_data="skate_yes"),
         InlineKeyboardButton(text="Нет ❌", callback_data="skate_no")],
        [InlineKeyboardButton(text="Отмена ❌", callback_data="user_cancel")]
    ]
)

helmet = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да ✅", callback_data="helmet_yes"),
         InlineKeyboardButton(text="Нет ❌", callback_data="helmet_no")],
        [InlineKeyboardButton(text="Отмена ❌", callback_data="user_cancel")]
    ]
)

defender = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да ✅", callback_data="defender_yes"),
         InlineKeyboardButton(text="Нет ❌", callback_data="defender_no")],
        [InlineKeyboardButton(text="Отмена ❌", callback_data="user_cancel")]
    ]
)

user_back_to_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться в меню 🏠", callback_data="user_back_to_menu")]
    ]
)

admin_back_to_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться в меню 🏠", callback_data="admin_cancel")]
    ]
)

admin_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад ⬅️", callback_data="admin_back_to_registration")]
    ]
)

admin_send_file = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Файл отсутствует 🚫", callback_data="file_no")],
        [InlineKeyboardButton(text="Отмена ❌", callback_data="admin_cancel")]
    ]
)