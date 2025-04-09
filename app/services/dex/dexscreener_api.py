import aiohttp

from config import DEXSCREENER_BASE_URL
from app.utils.dexscreeener_utils import filter_and_find_max_volume
from logging_config import setup_logger

logger = setup_logger("services-dex-dexscreener")


class DEXApi:
    def __init__(self):
        pass

    async def get_token_price_and_info(self, chain: str, token_addresses: str) -> str:
        url = DEXSCREENER_BASE_URL + f"/tokens/v1/{chain}/{token_addresses}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    detail = await response.json()
                    return await filter_and_find_max_volume(detail)
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при запросе к DEXAPI: {e}")
            return None
        except Exception as e:
            logger.error(f"Неожиданная ошибка DEX (get_token_price): {e}")
            return None
