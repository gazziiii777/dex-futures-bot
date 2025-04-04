from core.database_sqlalchemy import db_helper
from models.cex import MEXC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, and_, asc, delete, desc, func, select, update, or_



async def test(session: AsyncSession):
    quary = select(MEXC.name)
    res = await session.execute(quary)
    await session.commit()
    return {"names": list[*res]}