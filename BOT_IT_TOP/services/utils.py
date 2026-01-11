def format_list(title: str, items: list[str]) -> str:
    if not items:
        return f"{title}: Нет данных ✓"
    return f"{title}:\n" + "\n".join(items)

def format_dict(title: str, data: dict) -> str:
    if "error" in data:
        return f"Ошибка: {data['error']}"
    lines = [f"{k}: {v}" for k, v in data.items()]
    return f"{title}:\n" + "\n".join(lines)