import sqlite3

def calculate_price_change(symbol):  
    connection = sqlite3.connect("database/stock_mcp.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT price, timestamp FROM stock_data 
        WHERE symbol = ? 
        ORDER BY timestamp DESC 
        LIMIT 2
    """, (symbol,))
    # the first 2 rows ordered by time, where symbol is as provided as 1 element tuple input shall be selected

    results = cursor.fetchall()
    connection.close()

    if len(results) >= 2:
        current_price = results[0][0]
        previous_price = results[1][0]

        change = ((current_price - previous_price) / previous_price) * 100
        return round(change, 2), current_price, previous_price
    
    return None, None, None

def find_top_performer():
    stocks = ["AAPL", "GOOGL", "TSLA"]
    performance_data = []
    print("📊 Stock Performance Analysis:")
    print("-" * 50)
    for stock in stocks:
        change, current_price, previous_price = calculate_price_change(stock)

        if change is not None:
            performance_data.append((stock, change, current_price))
            # pure claude below:
            emoji = "🚀" if change > 0 else "📉" if change < 0 else "➡️"
            print(f"{emoji} {stock}: {change:+.2f}% (${current_price})")
            # : )))))
    
    if performance_data:
        best_stock = max(performance_data, key = lambda x:[1])
        print (f"\nTop performer: {best_stock[0]} with {best_stock[1]:+.2f}% gain!!!!")

    return performance_data

def get_market_summary():
    connection = sqlite3.connect("database/stock_mcp.db")
    
    cursor = connection.cursor()
    
    # Count total records
    cursor.execute("SELECT COUNT(*) FROM stock_data")
    total_records = cursor.fetchone()[0]
    
    # Get latest timestamp
    cursor.execute("SELECT MAX(timestamp) FROM stock_data")
    latest_update = cursor.fetchone()[0]
    
    print(f"\n📈 Market Summary:")
    print(f"📊 Total price records: {total_records}")
    print(f"🕐 Last update: {latest_update}")
    
    connection.close()

# Run the analysis
if __name__ == "__main__":
    find_top_performer()
    get_market_summary()