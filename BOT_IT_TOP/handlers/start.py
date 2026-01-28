from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()


def get_inline_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📅 Расписание", callback_data="report1"),
            InlineKeyboardButton(text="📘 Темы занятий", callback_data="report2")
        ],
        [
            InlineKeyboardButton(text="👨‍🎓 Проблемные студенты", callback_data="report3"),
            InlineKeyboardButton(text="📉 Посещаемость", callback_data="report4")
        ],
        [
            InlineKeyboardButton(text="📝 Проверка ДЗ (месяц)", callback_data="report5_month"),
            InlineKeyboardButton(text="📝 Проверка ДЗ (неделя)", callback_data="report5_week")
        ],
        [
            InlineKeyboardButton(text="📚 Выполнение ДЗ", callback_data="report6")
        ]
    ])


@router.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "👋 <b>Добро пожаловать!</b>\n\n"
        "Этот бот формирует отчёты по загруженным XLS/XLSX файлам.\n"
        "Выберите нужный отчёт из меню ниже."
    )

    await message.answer(text, reply_markup=get_inline_menu())
