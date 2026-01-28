from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

reports_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📅 Расписание", callback_data="report1")],
        [InlineKeyboardButton(text="📘 Темы занятий", callback_data="report2")],
        [InlineKeyboardButton(text="🏆 Проблемные студенты", callback_data="report3")],
        [InlineKeyboardButton(text="👥 Посещаемость", callback_data="report4")],
        [
            InlineKeyboardButton(text="📄 Проверка ДЗ (месяц)", callback_data="report5_month"),
            InlineKeyboardButton(text="📄 Проверка ДЗ (неделя)", callback_data="report5_week")
        ],
        [InlineKeyboardButton(text="📚 Выполнение ДЗ", callback_data="report6")],
    ]
)
