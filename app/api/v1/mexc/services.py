from core.database_sqlalchemy import db_helper
from models.cex import MEXC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, and_, asc, delete, desc, func, select, update, or_


session = db_helper.get_scoped_session()


async def test(session: AsyncSession):
    print(session)
    quary = select(MEXC)
