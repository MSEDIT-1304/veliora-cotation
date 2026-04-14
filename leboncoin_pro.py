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

            # ⏳ attendre chargement annonces
            page.wait_for_selector("a[data-qa-id='aditem_container']", timeout=15000)

            annonces = page.query_selector_all("a[data-qa-id='aditem_container']")

            for annonce in annonces:
                try:
                    text = annonce.inner_text()

                    match = re.search(r"(\d{3,6})\s?€", text)
                    if match:
                        price = int(match.group(1))

                        if 2000 < price < 100000:
                            prices.append(price)

                except:
                    continue

            browser.close()

        return prices[:30]

    except:
        return []
