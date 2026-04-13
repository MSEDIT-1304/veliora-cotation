import requests

def get_leboncoin_prices(brand, model, year, km, api_key):

    try:
        # 🔥 recherche Google (beaucoup plus fiable)
        query = f"{brand} {model} {year} {km} leboncoin prix"

        url = "https://api.scraperapi.com/"

        params = {
            "api_key": api_key,
            "url": f"https://www.google.com/search?q={query}",
            "render": "true"
        }

        response = requests.get(url, params=params)
        html = response.text

        prices = []

        # 🔎 extraction simple des prix
        for part in html.split("€"):
            try:
                price_str = part.split(">")[-1]
                price_str = price_str.replace(" ", "").replace("\xa0", "")

                price = int(price_str)

                if 2000 < price < 100000:
                    prices.append(price)

            except:
                continue

        # nettoyage
        prices = list(set(prices))[:15]

        return prices

    except Exception as e:
        print("Erreur Leboncoin :", e)
        return []
