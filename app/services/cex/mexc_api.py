import os

from pymexc import futures, spot
from core.config import settings


class MexcApi:
    def __init__(self):
        self.api_key = settings.MEXC_API_KEY
        self.secret_key = settings.MEXC_SECRET_KEY
        self.futures_client = futures.HTTP(
            api_key=self.api_key, api_secret=self.secret_key)
        self.spot_client = spot.HTTP(
            api_key=self.api_key, api_secret=self.secret_key)

    def get_detail(self):
        return self.futures_client.detail()

    def get_currency_info(self):
        return self.spot_client.get_currency_info()
