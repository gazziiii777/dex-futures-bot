import asyncio


async def all_futures_coins(futures_coins: list) -> dict:
    available_coins = []
    for coin in futures_coins:
        if coin.get('currency') == 'USDT':
            available_coins.append(coin.get('asset'))

    return available_coins
