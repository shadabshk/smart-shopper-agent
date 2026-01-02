import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def get_amazon_price(item_name: str) -> int | None:
    query = item_name.replace(" ", "+")
    url = f"https://www.amazon.in/s?k={query}"

    # First attempt
    resp = requests.get(url, headers=HEADERS, timeout=15)

    # Retry once if blocked or failed
    if resp.status_code != 200:
        print(f"⚠️ Amazon returned status {resp.status_code}, retrying once...")
        resp = requests.get(url, headers=HEADERS, timeout=15)

        if resp.status_code != 200:
            print(f"❌ Amazon failed after retry (status {resp.status_code})")
            return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Amazon price usually appears in this class
    price_tag = soup.select_one("span.a-price-whole")

    if not price_tag:
        print("⚠️ Amazon price not found")
        return None

    price_text = price_tag.get_text()
    price_text = re.sub(r"[^\d]", "", price_text)

    if not price_text:
        print("⚠️ Amazon price text empty after cleanup")
        return None

    return int(price_text)


# Manual test
if __name__ == "__main__":
    price = get_amazon_price("Dove Soap 125g")
    print("Amazon price:", price)
