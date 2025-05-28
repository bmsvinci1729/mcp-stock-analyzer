import yfinance as yf
import sqlite3
from datetime import datetime
import time

def get_real_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        current_price = info.get("currentPrice") or info.get("regularMarketPrice")

        # additional data
        volume = info.get("volume", 0)
        market_cap = info.get("marketCap", 0)
        pe_ratio = info.get("trailingPE", 0)
        hist = ticker.history(period="1d", interval="1m")

        if not hist.empty and current_price:
            latest_data = {
                'symbol': symbol,
                'price': round(float(current_price), 2),
                'volume': volume,
                'market_cap': market_cap,
                'pe_ratio': pe_ratio if pe_ratio else 0,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"✅ {symbol}: ${latest_data['price']} (Vol: {volume:,})")
            return latest_data

    except Exception as e:
        print(f"❌ Error fetching {symbol}: {e}")
    
    return None



def update_database_with_real_data():
    stock_symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "NVDA", "META"]
    connection = sqlite3.connect('database/stocks.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS real_stock_data (
            id INTEGER PRIMARY KEY,
            symbol TEXT NOT NULL,
            price REAL NOT NULL,
            volume INTEGER,
            market_cap INTEGER,
            pe_ratio REAL,
            timestamp TEXT NOT NULL
                   
        )
    ''')

    print("🔄 Fetching real stock data...")
    successful_updates = 0

    for symbol in stock_symbols:
        stock_data = get_real_stock_data(symbol)

        if stock_data:
            cursor.execute('''
                INSERT INTO real_stock_data (symbol, price, volume, market_cap, pe_ratio, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (stock_data['symbol'], stock_data['price'], stock_data['volume'], 
                  stock_data['market_cap'], stock_data['pe_ratio'], stock_data['timestamp']))
            successful_updates += 1

        time.sleep(2)

    connection.commit()
    connection.close()
    print(f"✅ Successfully updated {successful_updates} stocks in the database.")
    return successful_updates

if __name__ == "__main__":
    print("🚀 Starting REAL stock data collection...")
    update_database_with_real_data()