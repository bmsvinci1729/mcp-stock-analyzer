import requests
import time

def get_fake_stock_prices(symbol):
    """
        Nothing for now, dummy data only
    """
    import random
    base_prices = {
        "AAPL": 150.00,
        "GOOGL": 2800.00,
        "TSLA": 245.00
    }
    
    if symbol in base_prices:
        base = base_prices[symbol]
        var = random.uniform(-0.05, 0.05)
        new_price = base*(1 + var)
        return round(new_price, 2)
    
    return None

def test_scraper():
    print("Scraping stuff DUEDES\n")
    stocks = ["AAPL", "GOOGL", "TSLA"]
    
    for stock in stocks:
        price = get_fake_stock_prices(stock)
        print(f"📈 {stock}: ${price}")
        time.sleep(1)  # Wait 1 second between requests


# run tests
if __name__ == "__main__":
    test_scraper()
    