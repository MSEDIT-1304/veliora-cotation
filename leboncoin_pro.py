import requests
from bs4 import BeautifulSoup
import re

def get_leboncoin_prices(query, km=None, carburant=None, boite=None):
    try:
        url = f"https://www.leboncoin.fr/recherche?category=2&text={query}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        prices = []

        for span in soup.find_all("span"):
            text = span.get_text()

            if "€" in text:
                try:
                    price = int(re.sub(r"[^\d]", "", text))
                    
                    # filtre simple (évite valeurs absurdes)
                    if 1000 < price < 100000:
                        prices.append(price)

                except:
                    continue

        return prices[:30]

    except:
        return []
