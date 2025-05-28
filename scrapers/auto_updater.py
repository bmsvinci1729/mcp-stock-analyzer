import sqlite3 
import random
from datetime import datetime


def get_fake_stock_price(symbol):
    """Same fake price generator as before"""
    base_prices = {
        "AAPL": 150.00,
        "GOOGL": 2800.00,
        "TSLA": 245.00
    }
    
    if symbol in base_prices:
        base = base_prices[symbol]
        variation = random.uniform(-0.05, 0.05)
        new_price = base * (1 + variation)
        return round(new_price, 2)
    return None

def update_stock_price(symbol):
    """New price and save to the database"""
    # get new price
    new_price = get_fake_stock_price(symbol)

    if new_price:
        connection = sqlite3.connect("database/stock_mcp.db")
        cursor = connection.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "insert into stock_data (symbol, price, timestamp) VALUES (?, ?, ?)", (symbol, new_price, current_time)
        )
        
        connection.commit()
        connection.close()

        print(f"✅ Updated {symbol}: ${new_price}")


        return new_price
    
    return None


def update_all_stocks():
    # all tracked stocks to be updated
    stocks = ["AAPL", "GOOGL", "TSLA"]

    print(f"Updating stocks BOOM!!!")
    for stock in stocks:
        update_stock_price(stock)
    
    print ("YUP, DONE!!!")

if __name__ == "__main__":
    update_all_stocks()
