import pandas as pd
from pathlib import Path
from typing import List, Union
import re

def read_excel_safe(file_path: Path, header=0) -> Union[pd.DataFrame, str]:
    try:
        return pd.read_excel(file_path, header=header)
    except Exception as e:
        return f"Ошибка чтения файла: {e}"

def parse_schedule_week(file_path: Path) -> dict:
    df = read_excel_safe(file_path, header=None)
    if isinstance(df, str):
        return {"error": df}
    dates = []
    for col in df.iloc[0]:
        if isinstance(col, str) and "." in col and any(
                day in col.lower() for day in ["пон", "втор", "сред", "чет", "пят", "суб", "вос"]):
            dates.append(col.strip())

    group = None
    for val in df.iloc[:, 0].dropna():
        val = str(val).strip()
        if "/" in val:
            group = val
            break

    if not group:
        return {"error": "Не удалось определить группу в файле"}

    disciplines = {}

    for cell in df.values.flatten():
        if isinstance(cell, str) and "предмет:" in cell.lower():
            disc = cell.split(":", 1)[1].strip()
            disc = re.sub(r"\s+", " ", disc)  # убираем лишние пробелы и переносы
            disciplines[disc] = disciplines.get(disc, 0) + 1

    if not disciplines:
        return {"error": "Не найдено ни одной дисциплины в расписании"}

    sorted_disciplines = dict(sorted(disciplines.items(), key=lambda x: -x[1]))

    return {
        "group": group,
        "total_pairs": sum(sorted_disciplines.values()),
        "disciplines": sorted_disciplines,
        "dates": dates
    }

def parse_themes(file_path: Path) -> List[str]:
    df = read_excel_safe(file_path)
    if isinstance(df, str):
        return [df]

    df.columns = [str(c).lower() for c in df.columns]

    theme_col = next((c for c in df.columns if "тема" in c), None)
    if not theme_col:
        return ["Ошибка: колонка с темами не найдена"]

    invalid = []
    pattern = re.compile(r"^Урок №\s*\d+\.\s*Тема:\s+.+$", re.IGNORECASE)

    for theme in df[theme_col].dropna():
        t = str(theme).strip()
        if not pattern.match(t):
            invalid.append(t)

    return invalid

def parse_students(file_path: Path) -> List[str]:
    df = read_excel_safe(file_path)
    if isinstance(df, str):
        return [df]

    df.columns = [str(c).lower() for c in df.columns]

    fio_col = next((c for c in df.columns if "fio" in c or "фио" in c), None)
    hw_col = next((c for c in df.columns if "homew" in c or "дз" in c), None)
    class_col = next((c for c in df.columns if "class" in c or "класс" in c), None)

    if not fio_col or not hw_col or not class_col:
        return ["Ошибка: не найдены колонки ФИО, ДЗ или Классная работа"]

    bad = []

    for _, row in df.iterrows():
        fio = str(row.get(fio_col, "")).strip()
        if not fio:
            continue

        hw = pd.to_numeric(row.get(hw_col), errors="coerce")
        cr = pd.to_numeric(row.get(class_col), errors="coerce")

        if hw == 1 and cr < 3:
            bad.append(fio)

    return bad

def parse_attendance(file_path: Path) -> List[str]:
    df = read_excel_safe(file_path)
    if isinstance(df, str):
        return [df]

    df.columns = [str(c).lower() for c in df.columns]

    fio_col = next(
        (c for c in df.columns if "преподав" in c or "teacher" in c),
        None
    )
    att_col = next(
        (c for c in df.columns if "посещ" in c or "attend" in c or "%" in c),
        None
    )

    if not fio_col or not att_col:
        return ["Ошибка: не найдены колонки посещаемости или преподавателя"]

    low = []

    for _, row in df.iterrows():
        fio = str(row.get(fio_col, "")).strip()
        if not fio:
            continue

        att_raw = str(row.get(att_col, "")).replace("%", "").strip()
        att = pd.to_numeric(att_raw, errors="coerce")

        if pd.notna(att) and att < 40:
            low.append(f"{fio} ({att}%)")

    return low

def parse_checked_hw(file_path: Path) -> list[str]:
    df = read_excel_safe(file_path)
    if isinstance(df, str):
        return [df]


    df.columns = [str(c).strip().lower() for c in df.columns]


    teacher_col = next(
        (c for c in df.columns
         if "преподав" in c or "teacher" in c or "фио" in c or "препод" in c),
        None
    )


    issued_col = next(
        (c for c in df.columns
         if "выдано" in c or "issued" in c or "выд" in c),
        None
    )

    checked_col = next(
        (c for c in df.columns
         if "проверено" in c or "checked" in c or "пров" in c),
        None
    )


    if not teacher_col or not issued_col or not checked_col:
        first_row = [str(v).lower() for v in df.iloc[0].tolist()]

        if not teacher_col:
            for i, v in enumerate(first_row):
                if "преподав" in v or "teacher" in v or "фио" in v:
                    teacher_col = df.columns[i]

        if not issued_col:
            for i, v in enumerate(first_row):
                if "выдано" in v or "issued" in v or "выд" in v:
                    issued_col = df.columns[i]

        if not checked_col:
            for i, v in enumerate(first_row):
                if "проверено" in v or "checked" in v or "пров" in v:
                    checked_col = df.columns[i]


    if not teacher_col or not issued_col or not checked_col:
        return ["Ошибка: не найдены колонки преподавателя, выдано или проверено"]


    low = []

    for _, row in df.iterrows():
        teacher = str(row.get(teacher_col, "")).strip()
        if not teacher:
            continue

        issued = pd.to_numeric(row.get(issued_col), errors="coerce")
        checked = pd.to_numeric(row.get(checked_col), errors="coerce")

        if pd.notna(issued) and issued > 0:
            pct = (checked / issued) * 100 if pd.notna(checked) else 0
            if pct < 70:
                low.append(f"{teacher} — {pct:.1f}%")

    return low

def parse_completed_hw(file_path: Path) -> list[str]:
    df = read_excel_safe(file_path)
    if isinstance(df, str):
        return [df]

    df.columns = [str(c).strip().lower() for c in df.columns]

    fio_col = next(
        (c for c in df.columns
         if "фио" in c or "fio" in c or "name" in c or "student" in c),
        None
    )

    completed_col = next(
        (c for c in df.columns
         if "получено" in c or "сдан" in c or "done" in c or "completed" in c),
        None
    )

    issued_col = next(
        (c for c in df.columns
         if "выдано" in c or "issued" in c or "задано" in c or "total" in c),
        None
    )

    percent_col = next(
        (c for c in df.columns
         if "percent" in c or "percentage" in c or "%" in c or "процент" in c),
        None
    )

    if not fio_col or not (completed_col or percent_col):
        return ["Ошибка: не найдены колонки ФИО или данные по выполнению ДЗ"]

    low = []

    for _, row in df.iterrows():
        fio = str(row.get(fio_col, "")).strip()
        if not fio:
            continue

        if percent_col:
            pct_raw = str(row.get(percent_col, "")).replace("%", "").strip()
            pct = pd.to_numeric(pct_raw, errors="coerce")
        else:
            completed = pd.to_numeric(row.get(completed_col), errors="coerce")
            issued = pd.to_numeric(row.get(issued_col), errors="coerce")

            if pd.isna(completed) or pd.isna(issued) or issued == 0:
                continue

            pct = (completed / issued) * 100

        if pd.notna(pct) and pct < 70:
            low.append(f"{fio} — {pct:.1f}%")

    return low

