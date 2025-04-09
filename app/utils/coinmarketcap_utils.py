import asyncio


async def parse_coin_info(coin_info: dict, symbol: str) -> dict:
    coorect_coin_info = {}
    coorect_coin_info['name'] = coin_info.get('name')
    coorect_coin_info['symbol'] = coin_info.get('symbol')
    coorect_coin_info['slug'] = coin_info.get('slug')
    coorect_coin_info['logo'] = coin_info.get('logo')
    chains = []
    for chain in coin_info.get('contract_address'):
        contract_info = {}
        contract_info['token_address'] = chain.get('contract_address')
        slug_chain = chain.get('platform', {}).get('coin', {}).get('slug')
        contract_info['chain'] = 'bsc' if slug_chain == 'bnb' else slug_chain
        chains.append(contract_info)
    coorect_coin_info['contract_address'] = chains
    return coorect_coin_info
