# from app.models.cex import MEXC, BINGX
# from app.services.cex.mexc_api import MexcApi
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.exc import OperationalError
# from sqlalchemy import Result, and_, asc, delete, desc, func, select, update, text
# from sqlalchemy.sql.operators import ilike_op, or_, and_
# from sqlalchemy.orm import aliased
# from sqlalchemy.sql.expression import cast
from app.models.cex import MEXC
from core.database_sqlalchemy import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, and_, asc, delete, desc, func, select, update, or_
from sqlalchemy import exists, insert
from app.schemas.mexc import MEXCNewCoin, MEXCSymbol, MEXCUpdateSignal


# async def parse_crypto():
#     async with db_helper.scoped_session_dependency_context() as session:
#         mex_api = MexcApi()
#         main_mexc = await mex_api.get_all_futures_coin()

#         query = select(MEXC.name)
#         result = await session.execute(query)
#         names = [row[0] for row in result]
#         return names

async def is_coin_in_db(symbol: MEXCSymbol) -> bool:
    """Проверяет, есть ли монета с указанным именем в базе данных."""
    async with db_helper.scoped_session_dependency_context() as session:
        # Используем exists() для эффективной проверки
        query = select(
            exists().where(MEXC.symbol == symbol)
        )
        result = await session.execute(query)
        return result.scalar()  # Возвращает True или False

async def is_signal(symbol: MEXCSymbol) -> bool:
    """Проверяет, есть ли монета с указанным именем в базе данных."""
    async with db_helper.scoped_session_dependency_context() as session:
        # Используем exists() для эффективной проверки
        query = select(MEXC).where(and_(MEXC.signal == True, MEXC.symbol == symbol))
        result = await session.execute(query)
        return result.scalar()  # Возвращает True или False


async def insert_crypto_data(data: MEXCNewCoin) -> bool:
    """Добавляем новую монетку в БД, если она еще не существует"""
    async with db_helper.scoped_session_dependency_context() as session:
        # Проверяем, существует ли уже монета с таким символом
        existing_coin = await session.execute(
            select(MEXC).where(MEXC.symbol == data.get('symbol'))
        )
        if existing_coin.scalar_one_or_none() is not None:
            return False  # Монета уже существует

        # Если монеты нет, добавляем новую
        stmt = insert(MEXC).values(data)
        await session.execute(stmt)
        await session.commit()
        return True



async def is_coin_signal(symbol: MEXCSymbol) -> bool:
    """Проверяем доступна ли наша монетка для сиганлов"""
    async with db_helper.scoped_session_dependency_context() as session:
        query = select(
            exists().where(
                (MEXC.symbol == symbol) & (MEXC.signal == True)
            )
        )
        result = await session.execute(query)
        return result.scalar()


async def update_coin_signal(symbol: MEXCSymbol) -> bool:
    async with db_helper.scoped_session_dependency_context() as session:
        query = select(MEXC).where(MEXC.symbol == symbol)
        result = await session.execute(query)
        coin = result.scalar_one_or_none()
        if coin:
            coin.signal = False
            await session.commit()