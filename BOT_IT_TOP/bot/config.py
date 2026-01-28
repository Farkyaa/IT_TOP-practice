import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Не найден BOT_TOKEN в переменных окружения или .env файле")

BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / "temp"
LOG_DIR = BASE_DIR / "logs"

TEMP_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE = 20 * 1024 * 1024

ALLOWED_EXTENSIONS = {".xls", ".xlsx"}
