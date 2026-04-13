import requests
import re

def get_leboncoin_prices(query, km=None, carburant=None, boite=None):

    url = "https://api.scraperapi.com"

    params = {
        "api_key": "b21ec21db42b3d67cdd1d58d6c21c9bc",
        "url": f"https://www.ebay.fr/sch/i.html?_nkw={query.replace(' ', '+')}+voiture",
        "country_code": "fr"
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        html = response.text
    except:
        return []

    # extraction prix
    prices = re.findall(r'(\d{4,6})\s?€', html)

    prices = [int(p) for p in prices if 1000 < int(p) < 200000]

    prices = list(set(prices))

    return prices[:30]
