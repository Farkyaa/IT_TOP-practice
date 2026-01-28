import asyncio
import logging

from loader import bot, dp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

async def main():
    try:
        logging.info("Бот запущен. Ожидание сообщений...")
        await dp.start_polling(bot)

    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")

    finally:
        logging.info("Закрытие сессии бота...")
        await bot.session.close()
        logging.info("Бот остановлен.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем.")
