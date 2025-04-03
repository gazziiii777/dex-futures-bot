import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from config import settings


engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    # pool_size=5,
    # max_overflow=10
)


with engine.connect() as conn:
    res = conn.execute(text('SELECT VERSION()'))
    print(f"{res.first()}")
