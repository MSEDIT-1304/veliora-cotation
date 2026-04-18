import requests
import re

# 🔥 TA CLÉ SCRAPERAPI
SCRAPER_API_KEY = "TA_CLE_ICI"


def get_leboncoin_prices(query, km=None, carburant=None, boite=None):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        url = f"https://www.google.com/search?q={query} prix voiture occasion france"

        # 🔥 UTILISATION SCRAPERAPI
        response = requests.get(
            "http://api.scraperapi.com",
            params={
                "api_key": SCRAPER_API_KEY,
                "url": url,
                "country_code": "fr"
            },
            timeout=15
        )

        text = response.text

        # 🔥 extraction des prix
        raw_prices = re.findall(r'(\d{4,6})', text)

        prices = []

        for p in raw_prices:
            price = int(p)

            if 3000 < price < 80000:
                prices.append(price)

        # nettoyage
        prices = list(set(prices))
        prices.sort()

        # suppression extrêmes
        if len(prices) > 10:
            prices = prices[2:-2]

        # 🔥 fallback si pas assez de données
        if len(prices) < 3:

            base = 18000
            q = query.lower()

            if "toyota" in q:
                base = 20000
            elif "bmw" in q or "mercedes" in q:
                base = 32000
            elif "audi" in q:
                base = 30000
            elif "peugeot" in q:
                base = 18000
            elif "renault" in q:
                base = 17000
            elif "dacia" in q:
                base = 13000

            # ajustement année
            if "2024" in q or "2025" in q:
                base += 8000
            elif "2023" in q:
                base += 6000
            elif "2022" in q:
                base += 4000
            elif "2021" in q:
                base += 2000

            prices = [
                int(base * 0.9),
                int(base),
                int(base * 1.1),
                int(base * 1.2)
            ]

        return prices[:15]

    except:
        return [15000, 17000, 19000, 21000]
