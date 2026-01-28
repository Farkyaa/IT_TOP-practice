import logging
import os


from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import TEMP_DIR
from services.cache import get_cached_report
from services.validators import validate_excel_structure
from services.parsers import (
    parse_schedule_week, parse_themes, parse_students,
    parse_attendance, parse_checked_hw, parse_completed_hw
)
from services.report_formatters import (
    format_schedule_report,
    format_invalid_themes,
    format_problem_students,
    format_low_attendance,
    format_checked_hw,
    format_completed_hw
)

from keyboards.menu import menu_keyboard
from keyboards.inline_reports import reports_menu


router = Router()


class ReportState(StatesGroup):
    waiting_file = State()

async def request_file(message, state, report_type, prompt, extra=None):
    await message.answer(prompt, parse_mode=None)
    await state.set_state(ReportState.waiting_file)
    await state.update_data(report_type=report_type, extra=extra)


@router.callback_query()
async def report_menu(call: CallbackQuery, state: FSMContext):
    mapping = {
        "report1": (1, "Отправьте XLS/XLSX с расписанием группы на неделю."),
        "report2": (2, "Отправьте XLS/XLSX с темами занятий."),
        "report3": (3, "Отправьте XLS/XLSX с информацией по студентам."),
        "report4": (4, "Отправьте XLS/XLSX с посещаемостью преподавателей."),
        "report5_month": (5, "Отправьте XLS/XLSX с проверенными ДЗ (месяц).", "month"),
        "report5_week": (5, "Отправьте XLS/XLSX с проверенными ДЗ (неделя).", "week"),
        "report6": (6, "Отправьте XLS/XLSX с выполнением ДЗ студентами.")
    }

    cmd = call.data
    report_type, prompt, *extra = mapping[cmd]

    await request_file(call.message, state, report_type, prompt, extra[0] if extra else None)
    await call.answer()

@router.message(F.text == "📋 Меню отчётов")
async def show_menu(message: Message):
    await message.answer("Выберите отчёт:", reply_markup=None, parse_mode=None)
    await message.answer("Меню отчётов:", reply_markup=reports_menu, parse_mode=None)

@router.message(F.document, ReportState.waiting_file)
async def process_file(message: Message, state: FSMContext):
    data = await state.get_data()
    report_type = data.get("report_type")
    extra = data.get("extra")

    doc = message.document

    if not doc.file_name.lower().endswith((".xls", ".xlsx")):
        await message.answer("❗ Требуется файл формата .xls или .xlsx", parse_mode=None)
        return

    file_info = await message.bot.get_file(doc.file_id)
    file_path = TEMP_DIR / doc.file_name
    await message.bot.download_file(file_info.file_path, destination=file_path)

    logging.info(f"Получен файл: {doc.file_name}")

    try:
        structure_error = validate_excel_structure(report_type, file_path)
        if structure_error:
            await message.answer(f"❗ Ошибка структуры файла:\n{structure_error}", parse_mode=None)
            return

        cached = get_cached_report(report_type, file_path, extra)
        if cached:
            await message.answer("⚡ Использую кэшированный результат:", parse_mode=None)
            await message.answer(cached, parse_mode=None)
            return

        if report_type == 1:
            parsed = parse_schedule_week(file_path)
            text = format_schedule_report(parsed)

        elif report_type == 2:
            invalid = parse_themes(file_path)
            text = format_invalid_themes(invalid)

        elif report_type == 3:
            bad = parse_students(file_path)
            text = format_problem_students(bad)

        elif report_type == 4:
            low = parse_attendance(file_path)
            text = format_low_attendance(low)

        elif report_type == 5:
            low = parse_checked_hw(file_path)
            text = format_checked_hw(low)

        elif report_type == 6:
            low = parse_completed_hw(file_path)
            text = format_completed_hw(low)

        else:
            text = "Неизвестный тип отчёта"

        get_cached_report(report_type, file_path, extra, save=text)

        if len(text) > 4000:
            for chunk in [text[i:i + 4000] for i in range(0, len(text), 4000)]:
                await message.answer(chunk, parse_mode=None)
        else:
            await message.answer(text, parse_mode=None)

        await message.answer(
            "Выберите следующее действие:",
            reply_markup=menu_keyboard,
            parse_mode=None
        )

    except Exception as e:
        logging.error(f"Ошибка обработки отчёта {report_type}: {e}")
        await message.answer(f"❗ Ошибка при обработке файла:\n{e}", parse_mode=None)

    finally:
        if file_path.exists():
            os.remove(file_path)
        await state.clear()
