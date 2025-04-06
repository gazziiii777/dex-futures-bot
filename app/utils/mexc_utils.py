import asyncio


async def all_futures_coins(futures_coins: list) -> list[dict]:
    available_coins = []
    for coin in futures_coins:
        if coin.get('quoteCoin') == 'USDT':
            available_coins.append({
                'symbol' : coin.get('baseCoinName'),
                'logo' : coin.get('baseCoinIconUrl')
            })

    return available_coins
