from playwright.sync_api import sync_playwright
from playwright.sync_api import sync_playwright
import re
import random
import time

def get_leboncoin_prices(query, km=None, carburant=None, boite=None):

    prices = []

    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )

            page = context.new_page()

            url = f"https://www.leboncoin.fr/recherche?category=2&text={query}"

            page.goto(url, timeout=60000)

            # ⏳ simulation humaine
            time.sleep(random.uniform(2, 4))

            # scroll pour charger annonces
            page.mouse.wheel(0, 2000)
            time.sleep(2)

            elements = page.query_selector_all("a")

            for el in elements:
                try:
                    text = el.inner_text()

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
