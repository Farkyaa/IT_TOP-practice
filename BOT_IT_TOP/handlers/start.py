from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/report1"), KeyboardButton(text="/report2")],
            [KeyboardButton(text="/report3"), KeyboardButton(text="/report4")],
            [KeyboardButton(text="/report5_month"), KeyboardButton(text="/report5_week")],
            [KeyboardButton(text="/report6")],
        ],
        resize_keyboard=True
    )
    await message.answer("Добро пожаловать! Выберите отчёт:", reply_markup=keyboard)