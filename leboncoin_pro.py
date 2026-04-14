from playwright.sync_api import sync_playwright
import re

def get_leboncoin_prices(query, km=None, carburant=None, boite=None):

    prices = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            url = f"https://www.leboncoin.fr/recherche?category=2&text={query}"
            page.goto(url, timeout=60000)

            page.wait_for_timeout(3000)

            elements = page.query_selector_all("span")

            for el in elements:
                text = el.inner_text()

                if "€" in text:
                    try:
                        price = int(re.sub(r"[^\d]", "", text))

                        if 2000 < price < 100000:
                            prices.append(price)

                    except:
                        continue

            browser.close()

        return prices[:30]

    except:
        return []
