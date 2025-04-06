from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from urllib.parse import quote_plus
import json
import asyncio
from redis_config import get_redis_connection
import uuid

redis_conn = get_redis_connection()


def get_approve_keyboard(coin_data: dict) -> InlineKeyboardMarkup:
    # Подготавливаем callback данные

    data_id = str(uuid.uuid4())

    # Сохраняем данные на 1 час (3600 секунд)
    redis_conn.setex(
        name=f"coin:{data_id}",  # Префикс для удобства
        time=3600,
        value=json.dumps(coin_data)
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Добавить",
                    callback_data=f"add_{data_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=f"reject_{data_id}"
                )
            ]
        ]
    )
    return keyboard
