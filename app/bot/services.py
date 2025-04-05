from app.models.cex import MEXC, BINGX
from app.services.cex.mexc_api import MexcApi
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError
from sqlalchemy import Result, and_, asc, delete, desc, func, select, update, text
from sqlalchemy.sql.operators import ilike_op, or_, and_
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import cast



async def parse_crypto():
    mex_api = MexcApi()
    main_mexc = await mex_api.get_all_futures_coin()
    return main_mexc