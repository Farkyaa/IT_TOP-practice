from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Меню отчётов")]
    ],
    resize_keyboard=True
)
