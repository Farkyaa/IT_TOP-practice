from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.parsers import parse_schedule_week

from services.report_formatters import (
format_schedule_report,format_invalid_themes,format_problem_students)


from services.parsers import (
    parse_themes, parse_students, parse_attendance,
    parse_checked_hw, parse_completed_hw
)
from services.utils import format_list,
from config import TEMP_DIR

router = Router()

class ReportState(StatesGroup):
    waiting_file = State()

async def request_file(message: Message, state: FSMContext, report_type: int, prompt: str, extra: str = None):
    await message.answer(prompt)
    await state.set_state(ReportState.waiting_file)
    await state.update_data(report_type=report_type, extra=extra)

@router.message(Command("report1"))
async def cmd_report1(message: Message, state: FSMContext):
    await request_file(message, state, 1, "Отправьте XLS с расписанием группы на неделю.")

@router.message(Command("report2"))
async def cmd_report2(message: Message, state: FSMContext):
    await request_file(message, state, 2, "Отправьте XLS с темами занятий.")

@router.message(Command("report3"))
async def cmd_report3(message: Message, state: FSMContext):
    await request_file(message, state, 3, "Отправьте XLS с информацией по студентам.")

@router.message(Command("report4"))
async def cmd_report4(message: Message, state: FSMContext):
    await request_file(message, state, 4, "Отправьте XLS с посещаемостью по преподавателям.")

@router.message(Command("report5_month"))
async def cmd_report5_month(message: Message, state: FSMContext):
    await request_file(message, state, 5, "Отправьте XLS с проверенными ДЗ (за месяц).", extra='month')

@router.message(Command("report5_week"))
async def cmd_report5_week(message: Message, state: FSMContext):
    await request_file(message, state, 5, "Отправьте XLS с проверенными ДЗ (за неделю).", extra='week')

@router.message(Command("report6"))
async def cmd_report6(message: Message, state: FSMContext):
    await request_file(message, state, 6, "Отправьте XLS с сданными ДЗ студентами.")

@router.message(F.document, ReportState.waiting_file)
@router.message(F.document, ReportState.waiting_file)
async def process_file(message: Message, state: FSMContext):
    data = await state.get_data()
    report_type = data.get('report_type')
    extra = data.get('extra')

    if not message.document.file_name.lower().endswith(('.xls', '.xlsx')):
        await message.answer("Требуется файл .xls или .xlsx!")
        return

    file_info = await message.bot.get_file(message.document.file_id)
    file_path = TEMP_DIR / message.document.file_name

    await message.bot.download_file(file_info.file_path, destination=file_path)

    try:
        if report_type == 1:
            parsed_data = parse_schedule_week(file_path)
            text = format_schedule_report(parsed_data)


        elif report_type == 2:
            invalid_themes = parse_themes(file_path)
            text = format_invalid_themes(invalid_themes)


        elif report_type == 3:
            bad_students = parse_students(file_path)
            text = format_problem_students(bad_students)

        elif report_type == 4:
            low = parse_attendance(file_path)
            text = format_list("Преподаватели с посещаемостью < 40%:", low)

        elif report_type == 5:
            low_checked = parse_checked_hw(file_path, period=extra or 'month')
            text = format_list(f"Преподаватели с % проверенных ДЗ < 70% ({extra}):", low_checked)

        elif report_type == 6:
            low_students = parse_completed_hw(file_path)
            text = format_list("Студенты с % выполненных ДЗ < 70%:", low_students)

        else:
            text = "Неизвестный тип отчёта"

        if len(text) > 4000:
            for chunk in [text[i:i + 4000] for i in range(0, len(text), 4000)]:
                await message.answer(chunk)
        else:
            await message.answer(text)

    except Exception as e:
        await message.answer(f"Ошибка при обработке файла:\n{str(e)}")
        print(f"Ошибка report {report_type}: {e}")  # для отладки в консоль

    finally:
        if file_path.exists():
            file_path.unlink()
        await state.clear()