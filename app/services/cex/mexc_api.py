import os

from pymexc import futures, spot
from core.config import settings
import app.utils.mexc_utils as utils


class MexcApi:
    def __init__(self):
        self.api_key = settings.MEXC_API_KEY
        self.secret_key = settings.MEXC_SECRET_KEY
        self.futures_client = futures.HTTP(
            api_key=self.api_key, api_secret=self.secret_key)
        self.spot_client = spot.HTTP(
            api_key=self.api_key, api_secret=self.secret_key)

    async def get_all_futures_coin(self) -> list[dict]:
        detail = self.futures_client.detail()
        available_coins = await utils.all_futures_coins(detail.get('data'))
        return available_coins

    def get_currency_info(self):
        return self.spot_client.get_currency_info()
