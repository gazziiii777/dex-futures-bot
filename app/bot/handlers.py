from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from app.bot.services import is_coin_in_db
from app.services.cex.mexc_api import MexcApi
from app.services.oracles.coinmarketcap_api import CoinMarketCapApi
from .keyboard import get_approve_keyboard
from urllib.parse import unquote_plus
import json
import asyncio
from redis_config import get_redis_connection

redis_conn = get_redis_connection()


router = Router()


async def get_redis_data(data_id: str) -> dict:
    """Получаем данные из Redis"""
    data = redis_conn.get(f"coin:{data_id}")
    return json.loads(data) if data else None


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text='sdfsdf!')


@router.message(Command("parse"))
async def parse(message: Message):
    all_coins = await MexcApi().get_all_futures_coin()
    for coin in all_coins:
        symbol = coin.get('symbol')
        if await is_coin_in_db(symbol):
            await message.answer(text='yessss')
        else:
            coin_info_cmc = await CoinMarketCapApi().get_cryptocurrency_info(symbol)
            platform = coin_info_cmc.get('data').get(symbol)[
                0].get('platform')
            if platform == None:
                pass
            else:
                coin_data = {
                    "name": coin_info_cmc.get('data').get(symbol)[0].get('name'),
                    "symbol": symbol,
                    "slug": coin_info_cmc.get('data').get(symbol)[0].get('slug'),
                    "chain": platform.get('name'),
                    "token_address": platform.get('token_address'),
                    "logo": coin.get('logo'),
                    "signal": True
                }
                kb = get_approve_keyboard(coin_data)
                await message.answer(text=f"{platform}", reply_markup=kb)
                await asyncio.sleep(2)

    # print(zxc)
    # await message.answer(text=f"{zxc}")


@router.callback_query(F.data.startswith("add_"))
async def add_coin(callback: types.CallbackQuery):
    # 1. Получаем сериализованные данные (убираем префикс "add_")
    try:
        data_id = callback.data[4:]
        coin_data = await get_redis_data(data_id)
        print(coin_data)
    except:
        pass
