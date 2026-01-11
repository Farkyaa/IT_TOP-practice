def format_schedule_report(data: dict) -> str:
    if "error" in data:
        return f" {data['error']}"

    lines = [
        "📊 Отчёт по выставленному расписанию",
        f"Группа: {data['group']}",
        f"Всего пар за неделю: {data['total_pairs']}",
        "",
        "Количество пар по дисциплинам:"
    ]

    sorted_disc = sorted(data['disciplines'].items(), key=lambda x: x[1], reverse=True)

    for disc, count in sorted_disc:
        lines.append(f"  • {disc} — {count} пар")

    return "\n".join(lines)
def format_invalid_themes(themes: list[str]) -> str:
    if not themes:
        return " Все темы соответствуют формату «Урок №_. Тема: _»\nОтличная работа!"

    lines = [
        " Найдены темы, которые НЕ соответствуют формату «Урок №_. Тема: _»",
        "Всего проблемных тем: " + str(len(themes)),
        "─" * 60
    ]

    for i, theme in enumerate(themes, 1):
        lines.append(f" {i}. {theme}")
        lines.append("─" * 60)  # разделитель между уроками

    return "\n".join(lines)


def format_problem_students(students: list[str]) -> str:

    if not students:
        return " Проблемных студентов не найдено\n(ДЗ = 1 и классная < 3)"

    lines = [
        " **Проблемные студенты**",
        "(средняя ДЗ = 1 и классная работа ниже 3)",
        f"Всего: {len(students)}",
        "─" * 50
    ]

    for i, student in enumerate(students, 1):
        lines.append(f"{i}. {student}")

    lines.extend([
        "─" * 50,
        "Рекомендация: Провести беседу / назначить доп. занятия"
    ])

    return "\n".join(lines)