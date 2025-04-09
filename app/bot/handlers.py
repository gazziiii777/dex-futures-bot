from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from app.bot.services import is_coin_in_db, is_signal, update_coin_signal, insert_crypto_data
from app.services.cex.mexc_api import MexcApi
from app.services.oracles.coinmarketcap_api import CoinMarketCapApi
from app.services.dex.dexscreener_api import DEXApi
from .keyboard import get_approve_keyboard
from urllib.parse import unquote_plus
import json
import asyncio
from redis_config import get_redis_connection
import time
from aiogram.types import (
    Message,
    InputMediaPhoto,
)
from config import COINMARKETCAP_URL, MEXC_URL
from logging_config import setup_logger


logger = setup_logger('main')

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
    all_coins_from_mexc = await MexcApi().get_all_futures_coin()
    for coin_from_mexc in all_coins_from_mexc:
        symbol = coin_from_mexc.get('symbol')
        if await is_coin_in_db(symbol):
            pass
        else:
            coin_info_cmc = await CoinMarketCapApi().get_cryptocurrency_info(symbol)
            if type(coin_info_cmc) == dict:
                try:
                    logger.debug(
                        f"{coin_from_mexc.get('symbol')} - {coin_info_cmc}")
                    coin_data = {
                        "name": coin_info_cmc.get('name'),
                        "symbol": coin_info_cmc.get('symbol'),
                        "slug": coin_info_cmc.get('slug'),
                        "contract_address": coin_info_cmc.get('contract_address'),
                        "logo": coin_info_cmc.get('logo'),
                    }
                    img_cmc = coin_info_cmc.get('logo')
                    img_mexc = coin_from_mexc.get('logo')
                    try:
                        media = [
                            InputMediaPhoto(media=img_cmc),
                            InputMediaPhoto(media=img_mexc),
                        ]
                        await message.answer_media_group(media)
                    except Exception as e:
                        logger.error(
                            f"Ошибка: {e} при отправке изображения изображение с mexc {img_mexc} изображение с CMC {img_cmc} для монетки:{coin_info_cmc}")

                    kb = get_approve_keyboard(coin_data)
                    await message.answer(text=f"1. CoinMarketCap: {COINMARKETCAP_URL + coin_info_cmc.get('name').strip().replace(' ', '-').lower()}\n2. MEXC {MEXC_URL + symbol}_USDT\n\nLOGO: \n1. {img_cmc}\n2. {img_mexc}", reply_markup=kb, disable_web_page_preview=True)
                    time.sleep(10)
                except Exception as e:
                    logger.error(
                        f"Ошибка: {e} при отправке сообщения для монетки: {coin_info_cmc}")


@router.callback_query(F.data.startswith("add_"))
async def add_coin(callback: types.CallbackQuery):
    try:
        data_id = callback.data[4:]
        coin_data = await get_redis_data(data_id)
        coin_data.update({'signal': True})
        print(coin_data)
        await insert_crypto_data(coin_data)
        await callback.message.edit_text(
            text=f"✅ Монета {coin_data.get('name')} успешно добавлена!",
            reply_markup=None  # Убираем кнопки, если они были
        )
    except Exception as e:
        logger.error(f"Ошибка при добавлении монеты: {e}")
        await callback.message.edit_text(
            text="❌ Произошла ошибка при добавлении монеты.",
            reply_markup=None
        )


@router.callback_query(F.data.startswith("reject_"))
async def reject_coin(callback: types.CallbackQuery):
    # 1. Получаем сериализованные данные (убираем префикс "reject_")
    try:
        data_id = callback.data[7:]
        coin_data = await get_redis_data(data_id)
        coin_data.update({'signal': False})
        print(coin_data)
        await insert_crypto_data(coin_data)
        await callback.message.edit_text(
            text=f"❌ Монета {coin_data.get('name')} отклонена!",
            reply_markup=None  # Убираем кнопки, если они были
        )
    except Exception as e:
        logger.error(f"Ошибка при добавлении монеты: {e}")
        await callback.message.edit_text(
            text="❌ Произошла ошибка при добавлении монеты.",
            reply_markup=None
        )
