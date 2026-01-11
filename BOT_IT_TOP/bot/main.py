import asyncio
import logging

from loader import bot, dp
from handlers.start import router as start_router
from handlers.reports import router as reports_router

logging.basicConfig(level=logging.INFO)

dp.include_routers(start_router, reports_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем.")