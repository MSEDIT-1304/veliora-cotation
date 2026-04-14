import requests
import re

SCRAPER_API_KEY = "sk_ad_6UkihaYMO3C3ukRwDVFVpjV2"

def get_leboncoin_prices(query, km=None, carburant=None, boite=None):

    prices = []

    try:
        url = f"https://www.leboncoin.fr/recherche?category=2&text={query}"

        api_url = "https://api.scraperapi.com/"

        params = {
            "api_key": SCRAPER_API_KEY,
            "url": url,
            "render": "true"   # 🔥 IMPORTANT (JS activé)
        }

        response = requests.get(api_url, params=params, timeout=20)
        html = response.text

        for part in html.split("€"):
            try:
                price_str = part.split(">")[-1]
                price_str = re.sub(r"[^\d]", "", price_str)
                price = int(price_str)

                if 2000 < price < 100000:
                    prices.append(price)

            except:
                continue

        return prices[:30]

    except:
        return []
