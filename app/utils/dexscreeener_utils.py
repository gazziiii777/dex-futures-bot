async def filter_and_find_max_volume(data: dict) -> dict:
    filtered_items = []
    for item in data:
        if item['volume']['h24'] > 200000:
            filtered_items.append({
                'priceUsd': item['priceUsd'],
                'url': item['url'],
                'dexId': item['dexId'],
                'volume_h24': item['volume']['h24']
            })
        

    if not filtered_items:
        return None

    max_item = max(filtered_items, key=lambda x: x['volume_h24'])

    return max_item
