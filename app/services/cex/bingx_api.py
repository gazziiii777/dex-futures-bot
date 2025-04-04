import time
import aiohttp
import hmac
import os

from hashlib import sha256
from config import BINGX_BASE_URL
from core.config import settings


class BingXApi:
    def __init__(self):
        # Обратите внимание: у вас MEXC вместо BINGX
        self.api_key = settings.BINGX_API_KEY
        self.secret_key = settings.BINGX_SECRET_KEY  # Тут тоже MEXC
        self.base_url = BINGX_BASE_URL

    async def demo(self):
        payload = {}
        path = '/openApi/swap/v2/quote/contracts'
        method = "GET"
        params_map = {}
        params_str = self._parse_params(params_map)
        return await self._send_request(method, path, params_str, payload)

    def _get_sign(self, payload: str) -> str:
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            payload.encode("utf-8"),
            digestmod=sha256
        ).hexdigest()
        return signature

    async def _send_request(self, method: str, path: str, params_str: str, payload: dict):
        signature = self._get_sign(params_str)
        url = f"{self.base_url}{path}?{params_str}&signature={signature}"

        headers = {
            'X-BX-APIKEY': self.api_key,
        }

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, json=payload) as response:
                return await response.text()

    def _parse_params(self, params_map: dict) -> str:
        sorted_keys = sorted(params_map)
        params_str = "&".join([f"{k}={params_map[k]}" for k in sorted_keys])
        timestamp = f"timestamp={int(time.time() * 1000)}"

        if params_str:
            return f"{params_str}&{timestamp}"
        return timestamp
