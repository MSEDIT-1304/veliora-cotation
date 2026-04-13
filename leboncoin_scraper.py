import requests
import random
import time

def get_leboncoin_prices(query, km=None, carburant=None, boite=None):

    url = "https://api.leboncoin.fr/finder/search"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    payload = {
        "limit": 35,
        "offset": 0,
        "sort_by": "time",
        "sort_order": "desc",
        "filters": {
            "category": {"id": "2"},
            "enums": {},
            "keywords": query
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        data = response.json()
    except:
        return []

    prices = []

    try:
        ads = data.get("ads", [])
        for ad in ads:
            price = ad.get("price", [])
            if price:
                p = price[0]
                if 1000 < p < 200000:
                    prices.append(p)
    except:
        return []

    prices = list(set(prices))

    time.sleep(random.uniform(0.5, 1.5))

    return prices
