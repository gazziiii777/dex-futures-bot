import os

from dotenv import load_dotenv
from pymexc import futures

load_dotenv()


class MexcApi:
    def __init__(self):
        self.api_key = os.getenv('MEXC_API_KEY')
        self.secret_key = os.getenv('MEXC_SECRET_KEY')
        self.futures_client = futures.HTTP(
            api_key=self.api_key, api_secret=self.secret_key)

    def get_spot_client(self):
        return self.futures_client
