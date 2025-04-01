import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.api.exchanges.mexc.mexc_api import MexcApi
from aiogram.client.bot import DefaultBotProperties
from app.bot.handlers import router

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'),
          default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()


async def on_startup():
    """Функция, которая выполняется при запуске бота."""
    logging.info("Бот запущен.")


async def on_shutdown():
    """Функция, которая выполняется при остановке бота."""
    logging.info("Бот остановлен.")
    await bot.close()


async def main():
    """Основная функция, которая запускает бота и планировщик."""
    await on_startup()  # Выполняем startup-логику
    dp.include_router(router)
    await dp.start_polling(bot)  # Запускаем бота в режиме long-polling


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен вручную.")
    finally:
        asyncio.run(on_shutdown())  # Выполняем shutdown-логику
