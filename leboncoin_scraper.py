import requests
from bs4 import BeautifulSoup

def get_leboncoin_prices(brand, model, year, km, api_key):

    try:
        # 🔥 Recherche volontairement large (clé du succès)
        query = f"{brand} {model}"

        url = f"https://api.scraperapi.com/?api_key={api_key}&url=https://www.leboncoin.fr/recherche?text={query}"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        prices = []

        # 🔎 Sélection des prix (Leboncoin HTML)
        for span in soup.find_all("span"):
            text = span.get_text()

            if "€" in text:
                try:
                    price = int(
                        text.replace("€", "")
                        .replace(" ", "")
                        .replace("\xa0", "")
                    )
                    if 1000 < price < 100000:
                        prices.append(price)
                except:
                    pass

        # 🎯 Nettoyage (garde les valeurs cohérentes)
        prices = prices[:20]

        return prices

    except Exception as e:
        print("Erreur Leboncoin :", e)
        return []
