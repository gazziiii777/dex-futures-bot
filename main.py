from app.api.exchanges.mexc.mexc_api import MexcApi

a = MexcApi()
b = a.get_detail()
print(b)
