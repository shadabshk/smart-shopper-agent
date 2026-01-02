import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_flipkart_price(item_name: str) -> int | None:
    query = item_name.replace(" ", "%20")
    url = f"https://www.flipkart.com/search?q={query}"

    resp = requests.get(url, headers=HEADERS, timeout=15)
    if resp.status_code != 200:
        print("❌ Flipkart request failed")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # Flipkart price class
    price_tag = soup.select_one("div._30jeq3")

    if not price_tag:
        print("⚠️ Flipkart price not found")
        return None

    price_text = price_tag.get_text()
    price_text = re.sub(r"[^\d]", "", price_text)

    if not price_text:
        return None

    return int(price_text)

# Manual test
if __name__ == "__main__":
    price = get_flipkart_price("Dove Soap 125g")
    print("Flipkart price:", price)

