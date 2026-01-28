import pandas as pd
from pathlib import Path


def read_excel_header(file_path: Path):
    try:
        df = pd.read_excel(file_path, nrows=2)
        return df
    except Exception as e:
        return f"Ошибка чтения файла: {e}"


def validate_excel_structure(report_type: int, file_path: Path) -> str | None:
    df = read_excel_header(file_path)
    if isinstance(df, str):
        return df

    df.columns = [str(c).strip().lower() for c in df.columns]


    if report_type == 1:

        group_found = False
        for col in df.columns:
            values = df[col].dropna().astype(str)
            if any("/" in val or "рпо" in val.lower() for val in values):
                group_found = True
                break

        if not group_found:
            return "В файле не найдена колонка с группой)"

        return None

    if report_type == 2:
        if not any("тема" in c for c in df.columns):
            return "В файле должна быть колонка, содержащая слово «Тема»"
        return None

    if report_type == 3:
        cols = [str(c).lower() for c in df.columns]

        has_fio = any("fio" in c or "фио" in c for c in cols)
        has_hw = any("homew" in c or "дз" in c for c in cols)
        has_class = any("class" in c or "класс" in c for c in cols)

        missing = []
        if not has_fio:
            missing.append("фио / FIO")
        if not has_hw:
            missing.append("дз / Homework")
        if not has_class:
            missing.append("класс / Classroom")

        if missing:
            return (
                    "В файле отсутствуют необходимые колонки для отчёта №3:\n" +
                    "\n".join(f"• {m}" for m in missing)
            )

        return None

    if report_type == 4:
        cols = [str(c).lower() for c in df.columns]

        has_teacher = any("преподав" in c or "teacher" in c for c in cols)
        has_att = any("посещ" in c or "attend" in c or "%" in c for c in cols)

        missing = []
        if not has_teacher:
            missing.append("колонка преподавателя (содержит «преподав» или «teacher»)")
        if not has_att:
            missing.append("колонка посещаемости (содержит «посещ», «attend» или «%»)")

        if missing:
            return (
                    "В файле отсутствуют необходимые колонки для отчёта №4:\n" +
                    "\n".join(f"• {m}" for m in missing)
            )

        if report_type == 5:
            cols = [str(c).lower() for c in df.columns]

            has_issued = any("выдано" in c or "issued" in c for c in cols)
            has_checked = any("проверено" in c or "checked" in c for c in cols)

            if not has_issued or not has_checked:
                if len(df) > 0:
                    first_row = [str(v).lower() for v in df.iloc[0].tolist()]
                    has_issued = has_issued or any("выдано" in v or "issued" in v for v in first_row)
                    has_checked = has_checked or any("проверено" in v or "checked" in v for v in first_row)

            missing = []
            if not has_issued:
                missing.append("колонка «Выдано» / issued")
            if not has_checked:
                missing.append("колонка «Проверено» / checked")

            if missing:
                return (
                        "В файле отсутствуют необходимые колонки для отчёта №5:\n" +
                        "\n".join(f"• {m}" for m in missing)
                )

            return None

    if report_type == 6:
        cols = [str(c).strip().lower() for c in df.columns]

        has_fio = any(
            "фио" in c or "fio" in c or "name" in c or "student" in c
            for c in cols
        )

        if not has_fio:
            return (
                "В файле отсутствуют необходимые колонки для отчёта №6:\n"
                "• фио / FIO / name / student"
            )

        return None


    return None
