from price_check.amazon import get_amazon_price
from price_check.flipkart import get_flipkart_price

def select_cheapest(item_name: str, max_price: int):
    prices = {}

    amazon_price = get_amazon_price(item_name)
    if amazon_price:
        prices["Amazon"] = amazon_price

    flipkart_price = get_flipkart_price(item_name)
    if flipkart_price:
        prices["Flipkart"] = flipkart_price

    if not prices:
        print("❌ No prices found on any platform")
        return None, None

    platform = min(prices, key=prices.get)
    price = prices[platform]

    if price > max_price:
        print(f"⚠️ Cheapest price ₹{price} exceeds max price ₹{max_price}")
        return None, None

    print(f"✅ Selected {platform} at ₹{price}")
    return platform, price


# Manual test
if __name__ == "__main__":
    select_cheapest("Dove Soap 125g", max_price=500)

