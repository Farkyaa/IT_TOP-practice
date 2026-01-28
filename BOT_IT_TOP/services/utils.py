SEPARATOR = "─" * 60


def format_list(title: str, items: list[str]) -> str:
    if not items:
        return (
            f"📋 <b>{title}</b>\n"
            "Нет данных."
        )

    lines = [
        f"📋 <b>{title}</b>",
        SEPARATOR
    ]

    for i, item in enumerate(items, 1):
        lines.append(f"{i}. {item}")

    return "\n".join(lines)


def format_dict(title: str, data: dict) -> str:
    if "error" in data:
        return f"❗ Ошибка: {data['error']}"

    lines = [
        f"📘 <b>{title}</b>",
        SEPARATOR
    ]

    for key, value in data.items():
        lines.append(f"<b>{key}</b>: {value}")

    return "\n".join(lines)
