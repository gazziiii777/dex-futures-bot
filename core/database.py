from tortoise import Tortoise
from core.config import settings


TORTOISE_ORM = {
    "connections": {
        "default": settings.DATABASE_URL
    },
    "apps": {
        "models": {
            "models": ["models.first", "aerich.models"],
            "default_connection": "default",
        }
    }
}

async def init_db():
    """Инициализация базы данных"""
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

async def close_db():
    """Закрытие соединения с базой"""
    await Tortoise.close_connections()