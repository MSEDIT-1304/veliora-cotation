import requests

def get_leboncoin_prices(brand, model, year, km, api_key):

    try:
        query = f"{brand} {model}"

        url = "https://api.scraperapi.com/"

        params = {
            "api_key": api_key,
            "url": f"https://www.leboncoin.fr/recherche?category=2&text={query}",
            "render": "true"
        }

        response = requests.get(url, params=params)
        html = response.text

        prices = []

        # 🔥 Extraction simplifiée (fiable)
        for part in html.split("€"):
            try:
                price_str = part.split(">")[-1].replace(" ", "").replace("\xa0", "")
                price = int(price_str)

                if 1000 < price < 100000:
                    prices.append(price)

            except:
                continue

        # nettoyage
        prices = list(set(prices))[:20]

        return prices

    except Exception as e:
        print("Erreur Leboncoin :", e)
        return []
