import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple


def parse_schedule_week(file_path: Path) -> dict:
    try:
        df = pd.read_excel(file_path, header=None, dtype=str)

        if len(df) < 2:
            return {"error": "Файл слишком короткий, нет данных о группе"}

        group_cell = df.iloc[1, 0]
        if pd.isna(group_cell) or not isinstance(group_cell, str):
            return {"error": "Не удалось найти группу в файле (ожидается во второй строке)"}

        group = group_cell.strip()
        if len(group) < 5 or 'группа' in group.lower():

            for i in range(2, len(df)):
                val = df.iloc[i, 0]
                if pd.notna(val) and isinstance(val, str) and '/' in val:
                    group = val.strip()
                    break
            else:
                return {"error": "Не найдена реальная группа (нет строк с '/')"}

        disciplines = {}

        for _, row in df.iterrows():
            for cell in row:
                if pd.isna(cell):
                    continue
                text = str(cell).strip()
                if "Предмет:" in text:
                    try:
                        disc_part = text.split("Предмет:")[1].strip()
                        if "Группа:" in disc_part:
                            disc = disc_part.split("Группа:")[0].strip()
                        else:
                            disc = disc_part
                        disciplines[disc] = disciplines.get(disc, 0) + 1
                    except:
                        continue

        if not disciplines:
            return {"error": "Не найдено ни одной дисциплины"}

        return {
            "group": group,
            "total_pairs": sum(disciplines.values()),
            "disciplines": disciplines
        }

    except Exception as e:
        return {"error": f"Ошибка чтения файла: {str(e)}"}

def parse_themes(file_path: Path) -> List[str]:
    try:
        df = pd.read_excel(file_path)
        invalid = []
        theme_col = next((col for col in df.columns if 'тема' in col.lower()), None)
        if theme_col:
            for theme in df[theme_col].dropna():
                theme_str = str(theme).strip()
                if not (theme_str.startswith('Урок №') and 'Тема:' in theme_str):
                    invalid.append(theme_str)
        return invalid
    except Exception as e:
        return [f"Ошибка: {str(e)}"]


def parse_students(file_path: Path) -> list[str]:
    try:
        df = pd.read_excel(file_path)

        columns = df.columns.str.lower().str.strip()


        fio_col = next((col for col in columns if 'fio' in col or 'фио' in col), 'FIO')
        hw_col = next((col for col in columns if 'homework' in col or 'дз' in col.lower()), 'Homework')
        class_col = next((col for col in columns if 'classroom' in col or 'классн' in col.lower()), 'Classroom')

        bad_students = []

        for _, row in df.iterrows():
            fio = str(row.get(fio_col, '')).strip()
            if not fio:
                continue

            hw = pd.to_numeric(row.get(hw_col, pd.NA), errors='coerce')
            classroom = pd.to_numeric(row.get(class_col, pd.NA), errors='coerce')

            if pd.notna(hw) and pd.notna(classroom):
                if hw == 1 and classroom < 3:
                    bad_students.append(fio)

        return bad_students

    except Exception as e:
        return [f"Ошибка обработки файла: {str(e)}"]


def parse_attendance(file_path: Path) -> List[str]:
    try:
        df = pd.read_excel(file_path, header=1)
        low = []
        attendance_col = next((col for col in df.columns if 'посещаемость' in col.lower()), 'Средняя посещаемость')
        teacher_col = 'ФИО преподавателя'
        df[attendance_col] = df[attendance_col].str.rstrip('%').astype(float, errors='ignore')
        for _, row in df.iterrows():
            teacher = row.get(teacher_col, '').strip()
            att = row.get(attendance_col, 0)
            if teacher and att < 40:
                low.append(f"{teacher} ({att}%)")
        return low
    except Exception as e:
        return [f"Ошибка: {str(e)}"]


def parse_checked_hw(file_path: Path, period: str = 'month') -> List[str]:

    try:
        df = pd.read_excel(file_path, header=1)
        low = []

        if period == 'month':
            issued_col = 'Выдано'
            checked_col = 'Проверено'
        else:  # week
            issued_col = df.columns[7]
            checked_col = df.columns[9]

        for _, row in df.iterrows():
            teacher = str(row[1]).strip()
            if not teacher or pd.isna(teacher):
                continue
            issued = pd.to_numeric(row.get(issued_col, 0), errors='coerce')
            checked = pd.to_numeric(row.get(checked_col, 0), errors='coerce')
            if issued > 0:
                pct = (checked / issued) * 100
                if pct < 70:
                    low.append(f"{teacher} ({pct:.1f}%)")
        return low
    except Exception as e:
        return [f"Ошибка: {str(e)}"]


def parse_completed_hw(file_path: Path) -> List[str]:

    try:
        df = pd.read_excel(file_path, header=0)
        low = []
        pct_col = next((col for col in df.columns if 'percentage homework' in col.lower()), 'Percentage Homework')
        fio_col = 'FIO'
        df[pct_col] = pd.to_numeric(df[pct_col], errors='coerce')
        for _, row in df.iterrows():
            fio = row.get(fio_col, '').strip()
            pct = row.get(pct_col, 100)
            if fio and pct < 70:
                low.append(f"{fio} ({pct}%)")
        return low
    except Exception as e:
        return [f"Ошибка: {str(e)}"]