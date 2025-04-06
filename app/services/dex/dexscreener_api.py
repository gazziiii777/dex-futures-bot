import aiohttp

from config import DEXSCREENER_BASE_URL


class DEXApi:
    def __init__(self):
        pass

    async def get_token_price(self, chain: str, token_addresses: str) -> str:
        url = DEXSCREENER_BASE_URL + f"/tokens/v1/{chain}/{token_addresses}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    detail = await response.json()
                    return detail[0].get('priceUsd')
        except aiohttp.ClientError as e:
            print(f"Ошибка при запросе к DEXAPI: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка DEX (get_token_price): {e}")
            return None
