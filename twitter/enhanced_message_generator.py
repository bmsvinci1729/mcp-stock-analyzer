from datetime import datetime
import random

def create_real_market_alert(performance_data, alerts=None):
    """Create compelling Twitter message with real market data"""
    if not performance_data:
        return "📊 Market monitoring active - no significant moves detected."
    
    top_performer = performance_data[0]
    worst_performer = performance_data[-1] if len(performance_data) > 1 else None
    
    current_time = datetime.now().strftime("%H:%M")
    
    # Choose dynamic intro based on market conditions
    if top_performer['price_change'] > 5:
        intro = "🚀 MASSIVE MOVE ALERT"
    elif top_performer['price_change'] > 2:
        intro = "📈 STRONG PERFORMER"
    elif top_performer['price_change'] < -3:
        intro = "📉 MARKET DIP ALERT"
    else:
        intro = "📊 MARKET UPDATE"
    
    message = f"{intro} {current_time}\n"
    
    # Top performer section
    message += f"🏆 Leader: ${top_performer['symbol']}\n"
    message += f"💰 ${top_performer['current_price']} ({top_performer['price_change']:+.2f}%)\n"
    
    if top_performer['volume'] > 10000000:
        message += f"🔥 Volume: {top_performer['volume']:,}\n"
    
    # Add worst performer if significant drop
    if worst_performer and worst_performer['price_change'] < -2:
        message += f"📉 Laggard: ${worst_performer['symbol']} {worst_performer['price_change']:+.2f}%\n"
    
    # Add market alerts if any
    if alerts:
        alert_text = alerts[0].split(': ')[1] if ': ' in alerts[0] else alerts[0]
        message += f"⚡ {alert_text}\n"
    
    # Dynamic hashtags based on performance
    if top_performer['price_change'] > 3:
        hashtags = "#StockAlert #BullRun #Trading"
    elif top_performer['price_change'] < -2:
        hashtags = "#MarketDip #BuyTheDip #Stocks"
    else:
        hashtags = "#MarketUpdate #StockWatch #Investing"
    
    message += hashtags
    
    return message

def create_market_summary_tweet(performance_data):
    """Create broader market summary"""
    if not performance_data:
        return "📊 Market data collection in progress..."
    
    total_stocks = len(performance_data)
    gainers = [s for s in performance_data if s['price_change'] > 0]
    losers = [s for s in performance_data if s['price_change'] < 0]
    
    # Calculate market sentiment
    avg_change = sum([s['price_change'] for s in performance_data]) / total_stocks
    
    if avg_change > 1:
        sentiment = "🟢 BULLISH"
    elif avg_change < -1:
        sentiment = "🔴 BEARISH"
    else:
        sentiment = "🟡 MIXED"
    
    message = f"📊 MARKET SNAPSHOT\n"
    message += f"{sentiment} Sentiment\n"
    message += f"📈 Gainers: {len(gainers)}/{total_stocks}\n"
    message += f"📉 Decliners: {len(losers)}/{total_stocks}\n"
    message += f"📊 Avg Change: {avg_change:+.2f}%\n"
    
    if gainers:
        top_gainer = max(gainers, key=lambda x: x['price_change'])
        message += f"🚀 Top: ${top_gainer['symbol']} +{top_gainer['price_change']:.2f}%\n"
    
    message += "#MarketSummary #StockMarket #Trading"
    
    return message

def test_enhanced_messages():
    """Test with sample real-like data"""
    sample_data = [
        {'symbol': 'AAPL', 'current_price': 185.50, 'price_change': 3.2, 'volume': 45000000},
        {'symbol': 'TSLA', 'current_price': 248.75, 'price_change': -1.8, 'volume': 35000000},
        {'symbol': 'GOOGL', 'current_price': 2845.30, 'price_change': 0.9, 'volume': 15000000}
    ]
    
    sample_alerts = ["🔥 AAPL: High volume alert - 45,000,000 shares traded!"]
    
    print("🐦 Enhanced Twitter Message Generator Test:")
    print("-" * 50)
    
    alert_msg = create_real_market_alert(sample_data, sample_alerts)
    print("📱 Market Alert Tweet:")
    print(alert_msg)
    print()
    
    summary_msg = create_market_summary_tweet(sample_data)
    print("📊 Market Summary Tweet:")
    print(summary_msg)

# Test the enhanced messages
if __name__ == "__main__":
    test_enhanced_messages()
