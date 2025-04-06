from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from app.bot.services import is_coin_in_db, is_signal, update_coin_signal
from app.services.cex.mexc_api import MexcApi
from app.services.oracles.coinmarketcap_api import CoinMarketCapApi
from app.services.dex.dexscreener_api import DEXApi
from .keyboard import get_approve_keyboard
from urllib.parse import unquote_plus
import json
import asyncio
from redis_config import get_redis_connection
import time
from .services import insert_crypto_data
from aiogram.types import (
    Message,
    InputMediaPhoto,
)
from config import COINMARKETCAP_URL, MEXC_URL

redis_conn = get_redis_connection()


mex = MexcApi()

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
            coin_object = await is_signal(symbol)
            if coin_object:
                try:
                    price_dex, price_mexc = float(await DEXApi().get_token_price(coin_object.chain, coin_object.token_address)), float(await MexcApi().get_token_price(symbol=symbol))
                    if price_mexc is not None and price_dex is not None:
                        diff_percent = abs(price_mexc - price_dex) / price_mexc * 100
                        if diff_percent >= 2:
                            await message.answer(text=f"Price MEXC: {price_mexc}, price DEX: {price_dex}, delta: {diff_percent:.2f}% \n\nCoin with symbol - {symbol}\naddress- {coin_object.token_address}")
                    else:
                        print("❌ Cant parse price")
                except Exception as e:
                    await update_coin_signal(symbol=symbol)
                    await message.answer(text=f"Coin with symbol - {symbol}, chain = {coin_object.chain}, token_address = {coin_object.token_address} was deleted - {e}")

        else:
            coin_info_cmc = await CoinMarketCapApi().get_cryptocurrency_info(symbol)
            if type(coin_info_cmc) == dict:
                platform = coin_info_cmc.get('data').get(symbol)[
                    0].get('platform')
                if platform == None:
                    pass
                else:
                    name = coin_info_cmc.get('data').get(symbol)[0].get('name')
                    slug = coin_info_cmc.get('data').get(symbol)[0].get('slug')
                    chain = "bsc" if platform.get(
                        "slug") == "bnb" else platform.get("slug")
                    token_address = platform.get('token_address')
                    logo = coin.get('logo')
                    coin_data = {
                        "name": name,
                        "symbol": symbol,
                        "slug": slug,
                        "chain": chain,
                        "token_address": token_address,
                        "logo": logo,
                    }
                    img_cmc = coin_info_cmc.get('data').get(symbol)[
                        0].get('logo')
                    img_mexc = coin.get('logo')
                    media = [
                        InputMediaPhoto(media=img_cmc),
                        InputMediaPhoto(media=img_mexc),
                    ]
                    await message.answer_media_group(media)
                    kb = get_approve_keyboard(coin_data)
                    await message.answer(text=f"1. CoinMarketCap: {COINMARKETCAP_URL + name.replace(' ', '').lower()}\n2. MEXC {MEXC_URL + symbol}_USDT\n\nLOGO: \n1. {img_cmc}\n2. {img_mexc}", reply_markup=kb, disable_web_page_preview=True)
                    time.sleep(2)

    # print(zxc)
    # await message.answer(text=f"{zxc}")


@router.callback_query(F.data.startswith("add_"))
async def add_coin(callback: types.CallbackQuery):
    # 1. Получаем сериализованные данные (убираем префикс "add_")
    try:
        data_id = callback.data[4:]
        coin_data = await get_redis_data(data_id)
        coin_data.update({'signal': True})
        await insert_crypto_data(coin_data)
        await callback.message.edit_text(
            text=f"✅ Монета {coin_data.get('name')} успешно добавлена!",
            reply_markup=None  # Убираем кнопки, если они были
        )
    except:
        pass


@router.callback_query(F.data.startswith("reject_"))
async def add_coin(callback: types.CallbackQuery):
    # 1. Получаем сериализованные данные (убираем префикс "add_")
    try:
        data_id = callback.data[7:]
        coin_data = await get_redis_data(data_id)
        coin_data.update({'signal': False})
        await insert_crypto_data(coin_data)
        await callback.message.edit_text(
            text=f"❌ Монета {coin_data.get('name')} отклонена!",
            reply_markup=None  # Убираем кнопки, если они были
        )
    except:
        pass
