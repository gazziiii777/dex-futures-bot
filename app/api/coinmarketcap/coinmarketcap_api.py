import aiohttp
import asyncio
import os

from dotenv import load_dotenv
from config import COINMARKETCAP_BASE_URL

load_dotenv()


class CoinMarketCapApi:
    def __init__(self):
        self.api_key = os.getenv('COINMARKETCAP_API_KEY')
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }

    async def get_cryptocurrency_info(self, symbol: str) -> dict:
        """
        Асинхронно получает метаданные криптовалют с CoinMarketCap API v2

        Параметры:
            api_key: ваш API-ключ CoinMarketCap
            ids: строка с ID криптовалют (через запятую)
            slugs: строка с slug'ами криптовалют (через запятую)
            symbols: строка с символами криптовалют (через запятую)
            address: контрактный адрес токена
            skip_invalid: пропускать невалидные записи
            aux: дополнительные поля данных

        Возвращает:
            Словарь с ответом API или None в случае ошибки
        """
        url = COINMARKETCAP_BASE_URL + "/v2/cryptocurrency/info"

        params = {
            'symbol': symbol
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, params=params) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            print(f"Ошибка при запросе к API CoinMarketCap: {e}")
            return None
        except Exception as e:
            print(
                f"Неожиданная ошибка CoinMarketCapApi (get_cryptocurrency_info): {e}")
            return None
