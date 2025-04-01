import aiohttp

from dotenv import load_dotenv
from config import DEXSCREENER_BASE_URL

load_dotenv()


class DEXApi:

    async def get_token_price(self, chainId: str, tokenAddresses: str) -> dict:

        url = DEXSCREENER_BASE_URL + f"/tokens/v1/{chainId}/{tokenAddresses}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            print(f"Ошибка при запросе к DEXAPI: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка DEX (get_token_price): {e}")
            return None
