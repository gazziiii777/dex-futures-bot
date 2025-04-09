# from app.models.cex import MEXC, BINGX
# from app.services.cex.mexc_api import MexcApi
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.exc import OperationalError
# from sqlalchemy import Result, and_, asc, delete, desc, func, select, update, text
# from sqlalchemy.sql.operators import ilike_op, or_, and_
# from sqlalchemy.orm import aliased
# from sqlalchemy.sql.expression import cast
from app.models.cex import MEXC, Chains
from core.database_sqlalchemy import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, and_, asc, delete, desc, func, select, update, or_
from sqlalchemy import exists, insert
from app.schemas.mexc import MEXCNewCoin, MEXCSymbol, MEXCUpdateSignal

from logging_config import setup_logger

logger = setup_logger('services')

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
        query = select(MEXC).where(
            and_(MEXC.signal == True, MEXC.symbol == symbol))
        result = await session.execute(query)
        return result.scalar()  # Возвращает True или False


async def insert_crypto_data(data: dict) -> bool:
    """Добавляем новую монетку и связанные цепочки в БД, если она еще не существует"""
    async with db_helper.scoped_session_dependency_context() as session:
        coin_name = data.get('name')
        coin_symbol = data.get('symbol')
        coin_slug = data.get('slug')
        coin_logo = data.get('logo')
        coin_signal = data.get('signal')
        

        existing_coin = await session.execute(
            select(MEXC).where(MEXC.symbol == coin_symbol)
        )
        if existing_coin.scalar_one_or_none() is not None:
            return False  


        mexc_obj = MEXC(
            name=coin_name,
            symbol=coin_symbol,
            slug=coin_slug,
            logo=coin_logo,
            signal=coin_signal
        )


        if 'contract_address' in data:  
            for contract in data['contract_address']:  
                chain_obj = Chains(
                    chain=contract.get("chain"),
                    token_address=contract.get("token_address"),
                    mexc=mexc_obj
                )
                session.add(chain_obj)

        # Сохраняем монету в базе
        session.add(mexc_obj)
        await session.commit()
        logger.info(f"✅ Добавили монету: {coin_symbol}")  # Используем переменную
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


# async def save_coin_with_chains(session: AsyncSession, coin_data: dict, coin_info_cmc: dict):
#     mexc_obj = MEXC(
#         name=coin_info_cmc.get('name'),
#         symbol=coin_info_cmc.get('symbol'),
#         slug=coin_info_cmc.get('slug'),
#         logo=coin_info_cmc.get('logo'),
#         signal=False
#     )

#     contract_addresses = coin_info_cmc.get('contract_address', [])
#     for contract in contract_addresses:
#         chain_obj = Chains(
#             chain=contract.get('chain'),
#             token_address=contract.get('token_address'),
#             mexc=mexc_obj
#         )
#         session.add(chain_obj)

#     session.add(mexc_obj)
#     await session.commit()
#     logger.info(f"✅ Сохранили монету {mexc_obj.symbol} с {len(contract_addresses)} цепочками")


# async def parse_1():
#     async with db_helper.scoped_session_dependency_context() as session:
#         all_coins = await MexcApi().get_all_futures_coin()
#         for coin in all_coins:
#             symbol = coin.get('symbol')
#             logger.info(f"🔍 Обрабатываем монету: {symbol}")

#             if await is_coin_in_db(session, symbol):
#                 logger.info(f"⏭️ Монета {symbol} уже есть в базе")
#                 continue

#             coin_info_cmc = await CoinMarketCapApi().get_cryptocurrency_info(symbol)
#             print(coin_info_cmc)
#             if not coin_info_cmc:
#                 logger.warning(f"⚠️ Нет данных от CMC для {symbol}")
#                 continue

#             await save_coin_with_chains(session, coin, coin_info_cmc)
#             await asyncio.sleep(2)
