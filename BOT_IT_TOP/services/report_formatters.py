SEPARATOR = "─" * 60

def format_schedule_report(data: dict) -> str:
    if "error" in data:
        return f"❗ Ошибка: {data['error']}"

    group = data["group"]
    total = data["total_pairs"]
    dates = data.get("dates", [])

    if dates:
        dates_block = "\n".join([f"• {d}" for d in dates])
    else:
        dates_block = "• Даты не определены"

    lines = [
        f"📊 Аналитика расписания — группа {group}",
        "",
        "🗓️ Даты занятий:",
        dates_block,
        "",
        f"📚 Всего учебных пар: {total}",
    ]

    return "\n".join(lines)

def format_invalid_themes(themes: list[str]) -> str:
    if not themes:
        return (
            "✅ <b>Все темы соответствуют формату</b>\n"
            "«Урок № _. Тема: _»"
        )

    lines = [
        "⚠️ <b>Найдены темы, которые НЕ соответствуют формату</b>",
        "Формат: «Урок № _. Тема: _»",
        f"Всего проблемных тем: <b>{len(themes)}</b>",
        SEPARATOR
    ]

    for i, theme in enumerate(themes, 1):
        lines.append(f"{i}. {theme}")
        lines.append(SEPARATOR)

    return "\n".join(lines)

def format_problem_students(students: list[str]) -> str:
    if not students:
        return (
            "✅ <b>Проблемных студентов не найдено</b>\n"
            "(ДЗ = 1 и классная работа < 3)"
        )

    lines = [
        "🚨 <b>Проблемные студенты</b>",
        "(средняя ДЗ = 1 и классная работа ниже 3)",
        f"Всего: <b>{len(students)}</b>",
        SEPARATOR
    ]

    for i, student in enumerate(students, 1):
        lines.append(f"{i}. {student}")

    return "\n".join(lines)

def format_low_attendance(teachers: list[str]) -> str:
    if not teachers:
        return "✅ <b>Нет преподавателей с посещаемостью ниже 40%</b>"

    lines = [
        "📉 <b>Низкая посещаемость</b>",
        "Преподаватели с посещаемостью ниже 40%",
        f"Всего: <b>{len(teachers)}</b>",
        SEPARATOR
    ]

    for i, t in enumerate(teachers, 1):
        lines.append(f"{i}. {t}")

    return "\n".join(lines)

def format_checked_hw(teachers: list[str]) -> str:
    if not teachers:
        return "✅ <b>Все преподаватели проверяют ДЗ более чем на 70%</b>"

    lines = [
        "📝 <b>Низкий процент проверенных ДЗ</b>",
        "Преподаватели с процентом проверки ниже 70%",
        f"Всего: <b>{len(teachers)}</b>",
        SEPARATOR
    ]

    for i, t in enumerate(teachers, 1):
        lines.append(f"{i}. {t}")

    return "\n".join(lines)

def format_completed_hw(students: list[str]) -> str:
    if not students:
        return "✅ <b>Все студенты выполняют ДЗ более чем на 70%</b>"

    lines = [
        "📘 <b>Низкий процент выполнения ДЗ</b>",
        "Студенты, выполнившие менее 70% заданий",
        f"Всего: <b>{len(students)}</b>",
        SEPARATOR
    ]

    for i, s in enumerate(students, 1):
        lines.append(f"{i}. {s}")

    return "\n".join(lines)
