import requests
from bs4 import BeautifulSoup
import re

def get_leboncoin_prices(query, km=None, carburant=None, boite=None):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        url = f"https://www.google.com/search?q={query} voiture occasion prix"

        response = requests.get(url, headers=headers, timeout=10)
        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        prices = []

        # 🔥 méthode + large
        texts = soup.get_text()

        matches = re.findall(r'\d{4,6}', texts)

        for m in matches:
            price = int(m)

            if 2000 < price < 100000:
                prices.append(price)

        # 🔥 nettoyage
        prices = list(set(prices))
        prices.sort()

        return prices[:15]

    except Exception as e:
        print("Erreur scraper :", e)
        return []
