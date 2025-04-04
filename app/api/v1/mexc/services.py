from core.database_sqlalchemy import db_helper
from app.models.cex import MEXC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, and_, asc, delete, desc, func, select, update, or_


async def test(session: AsyncSession):
    query = select(MEXC.name)  # Исправлено опечатку "quary" -> "query"
    result = await session.execute(query)
    names = [row[0] for row in result]  # Правильное извлечение значений
    return {"names": names}
