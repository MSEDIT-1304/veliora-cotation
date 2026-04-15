import requests
from bs4 import BeautifulSoup
import re

def extract_price(text):
    try:
        text = text.replace("\xa0", "").replace(" ", "")
        match = re.search(r"(\d{4,6})", text)
        if match:
            return int(match.group(1))
    except:
        return None
    return None


def get_leboncoin_prices(query, km=None, carburant=None, boite=None):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        url = f"https://www.google.com/search?q={query} prix voiture occasion"

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        prices = []

        # 🔥 récupération intelligente des prix
        for element in soup.find_all(text=re.compile("€")):
            price = extract_price(element)

            if price and 2000 < price < 100000:
                prices.append(price)

        # 🔥 suppression doublons
        prices = list(set(prices))

        # 🔥 tri
        prices = sorted(prices)

        # 🔥 sécurité : minimum data sinon rejet
        if len(prices) < 3:
            return []

        # 🔥 limiter à 15 valeurs max
        return prices[:15]

    except Exception as e:
        print("Erreur scraper :", e)
        return []
