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


def normalize(text):
    return text.lower().replace("-", " ").replace("/", " ")


def get_leboncoin_prices(query, km=None, carburant=None, boite=None):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        url = f"https://www.google.com/search?q={query} leboncoin voiture"

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        prices = []

        # 🔥 récupération blocs texte (plus propre)
        results = soup.find_all("div")

        for r in results:
            text = r.get_text(" ", strip=True)

            if "€" not in text:
                continue

            price = extract_price(text)
            if not price:
                continue

            # 🔥 FILTRAGE INTELLIGENT

            text_norm = normalize(text)

            # filtre carburant
            if carburant and carburant.lower() not in text_norm:
                continue

            # filtre boîte
            if boite:
                if boite == "Automatique" and "auto" not in text_norm:
                    continue
                if boite == "Manuelle" and "manuelle" not in text_norm:
                    continue

            # filtre km
            if km:
                km_match = re.search(r"(\d{4,6})\s?km", text_norm)
                if km_match:
                    km_value = int(km_match.group(1))
                    if abs(km_value - km) > 40000:
                        continue

            # filtre prix réaliste
            if 3000 < price < 100000:
                prices.append(price)

        # 🔥 nettoyage
        prices = list(set(prices))
        prices.sort()

        # fallback intelligent (mais PAS aléatoire)
        if len(prices) < 3:
            return []

        return prices[:20]

    except Exception as e:
        print("Erreur scraper PRO :", e)
        return []
