import sqlite3

from datetime import datetime, timedelta

def calculate_real_performane(symbol, timeframe_minutes = 2):
    connection = sqlite3.connect("database/stocks.db")
    cursor = connection.cursor()

    # getting data from last timeframe
    cutoff_time = datetime.now() - timedelta(minutes=timeframe_minutes)
    cutoff_str = cutoff_time.strftime("%Y-%m-%d %H:%M:%S")

    # querqying the recent / latest changes in PRICE and VOLUME captured from the scraper
    cursor.execute("""
        SELECT price, volume, timestamp FROM real_stock_data 
        WHERE symbol = ? AND timestamp >= ?
        ORDER BY timestamp DESC
    """, (symbol, cutoff_str))
    
    results = cursor.fetchall()
    connection.close()

    if len(results) >= 2:
        current_price = results[0][0]
        current_volume = results[0][1]
        oldest_price = results[-1][0]


        change = ((current_price - oldest_price)/ oldest_price) * 100
        avg_volume = sum([row[1] for row in results]) / len(results)

        return {
            'symbol': symbol,
            'current_price': current_price,
            'volume': current_volume,
            'price_change': round(change, 2),
            'avg_volume': round(avg_volume, 2),
            'data_points': len(results)
        }
    return None

def find_real_top_performers(timeframe_minutes = 2):
    connection = sqlite3.connect("database/stocks.db")
    cursor = connection.cursor()

    # getting data from last timeframe
    cutoff_time = datetime.now() - timedelta(minutes=timeframe_minutes)
    cutoff_str = cutoff_time.strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        SELECT DISTINCT symbol FROM real_stock_data 
        WHERE timestamp >= ?
        GROUP BY symbol
    """, (cutoff_str,))

    symbols = [row[0] for row in cursor.fetchall()]
    connection.close()
    print(f"📊 Analyzing {len(symbols)} stocks over last {timeframe_minutes} minutes...")
    print("-" * 60)
    performance_data = []
    for symbol in symbols:
        perf = calculate_real_performane(symbol, timeframe_minutes)
        if perf:
            performance_data.append(perf)
            # Display with appropriate emoji
            if perf['price_change'] > 2:
                emoji = "🚀"
            elif perf['price_change'] > 0:
                emoji = "📈"
            elif perf['price_change'] < -2:
                emoji = "📉"
            else:
                emoji = "➡️"
            
            print(f"{emoji} {symbol}: {perf['price_change']:+.2f}% (${perf['current_price']}) Vol: {perf['volume']:,}")
    
    # Sort by performance
    performance_data.sort(key=lambda x: x['price_change'], reverse=True)
    
    if performance_data:
        print(f"\n🏆 TOP PERFORMER: {performance_data[0]['symbol']} with {performance_data[0]['price_change']:+.2f}% gain!")
        print(f"📉 WORST PERFORMER: {performance_data[-1]['symbol']} with {performance_data[-1]['price_change']:+.2f}% change!")
    
    return performance_data


def get_market_alerts():
    connection = sqlite3.connect("database/stocks.db")
    cursor = connection.cursor()

    cursor.execute("""
         SELECT symbol, price, volume, timestamp,
               ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY timestamp DESC) as rn
        FROM real_stock_data
    """)
    
    latest_data = [row for row in cursor.fetchall() if row[4] == 1] # rn = 1 means latest entry for each symbol

    alerts = []

    for symbol, price, volume, timestamp, rn in latest_data:
        if volume > 50000000:
            alerts.append(f"🔥 {symbol}: High volume alert - {volume:,} shares traded!")
        if price > 1000:
            alerts.append(f"💎 {symbol}: High-value stock at ${price}")
    
    connection.close()
    return alerts

if __name__ == "__main__":
    print("🔍 Real-Time Market Analysis Starting...")
    
    # Analyze performance
    performers = find_real_top_performers(10)
    
    # Get market alerts
    alerts = get_market_alerts()
    
    if alerts:
        print(f"\n🚨 MARKET ALERTS:")
        for alert in alerts:
            print(alert)
    
    print(f"\n📊 Analysis complete - {len(performers)} stocks analyzed")