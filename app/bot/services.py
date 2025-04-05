from app.models.cex import MEXC, BINGX
from app.services.cex.mexc_api import MexcApi
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError
from sqlalchemy import Result, and_, asc, delete, desc, func, select, update, text
from sqlalchemy.sql.operators import ilike_op, or_, and_
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import cast
from app.models.cex import MEXC
from core.database_sqlalchemy import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, and_, asc, delete, desc, func, select, update, or_





async def parse_crypto():
    async with db_helper.scoped_session_dependency_context() as session:
        mex_api = MexcApi()
        main_mexc = await mex_api.get_all_futures_coin()

        query = select(MEXC.name)
        result = await session.execute(query)
        names = [row[0] for row in result]
        return names
