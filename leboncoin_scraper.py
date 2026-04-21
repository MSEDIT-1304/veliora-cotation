import requests
import re
import statistics

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_leboncoin_prices(query, km=None, carburant=None, boite=None):

    try:
        km_str = f"{int(km)}km" if km else ""
        carburant_str = carburant if carburant else ""
        boite_str = boite if boite else ""

        search_query = f"{query} {km_str} {carburant_str} {boite_str} occasion"
        url = f"https://www.leboncoin.fr/recherche?text={search_query}"

        response = requests.get(url, headers=HEADERS, timeout=10)
        html = response.text

        raw_prices = re.findall(r'(\d{2,3}[ ]?\d{3}) ?€', html)

        prices = []

        for p in raw_prices:
            price = int(p.replace(" ", ""))
            if 4000 < price < 80000:
                prices.append(price)

        prices = list(set(prices))
        prices.sort()

        if len(prices) >= 5:
            median = statistics.median(prices)
            prices = [p for p in prices if (median * 0.7) < p < (median * 1.3)]

        # fallback propre
        if len(prices) < 4:
            return []

        return prices[:10]

    except:
        return []

