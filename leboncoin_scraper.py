import requests
import re
import random
import time

SCRAPER_API_KEY = "b21ec21db42b3d67cdd1d58d6c21c9bc"

def get_leboncoin_prices(query, km=None, carburant=None, boite=None):
    
    search_url = f"https://www.leboncoin.fr/recherche?text={query.replace(' ', '+')}&category=2"
    
    payload = {
        "api_key": SCRAPER_API_KEY,
        "url": search_url,
        "country_code": "fr",
        "render": "true"
    }

    try:
        response = requests.get("http://api.scraperapi.com", params=payload, timeout=60)
        html = response.text
    except:
        return []

    prices = re.findall(r'(\d{4,6})\s?€', html)

    prices = [int(p) for p in prices if int(p) > 1000 and int(p) < 200000]

    prices = list(set(prices))

    if len(prices) < 5:
        return prices

    time.sleep(random.uniform(1, 2))

    return prices[:30]
