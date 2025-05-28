from datetime import datetime

def create_stock_alert_message(top_performer_data):
    if not top_performer_data:
        return "Market update: No significant changes observed"
    
    best_stock, best_change, best_price = top_performer_data[0]
    if best_change > 2:
        emoji = "🚀"
        action = "soaring"
    elif best_change > 0:
        emoji = "📈"
        action = "rising"
    elif best_change < -2:
        emoji = "📉"
        action = "dropping"
    else:
        emoji = "➡️"
        action = "stable"
    
    current_time = datetime.now().strftime("%H:%M")
    
    message = f"{emoji} STOCK ALERT {current_time}\n"
    message += f"🏆 Top performer: ${best_stock}\n"
    message += f"💰 Price: ${best_price}\n"
    message += f"📊 Change: {best_change:+.2f}%\n"
    message += f"🔥 Stock is {action}!\n"
    message += "#StockAlert #Trading #MarketUpdate"

    return message

def create_market_summary(all_performance_data):
    if not all_performance_data:
        return "📊 Market data unavailable"
    
    total_stocks = len(all_performance_data)
    gainers = [stock for stock in all_performance_data if stock[1] > 0]
    losers = [stock for stock in all_performance_data if stock[1] < 0] # change

    message = f"📊 MARKET SNAPSHOT\n"
    message += f"📈 Gainers: {len(gainers)}/{total_stocks}\n"
    message += f"📉 Losers: {len(losers)}/{total_stocks}\n"

    if gainers:
        best_gainer = max(gainers, key = lambda x: x[1])
        message += f" Best : {best_gainer[0]}+{best_gainer[1]:.2f}%\n"
    
    message += "#MarketSummary #StockMarket"

    return message

def test_message_generator():
    test_data = [
        ("AAPL", 2.5, 152.30),
        ("GOOGL", -1.2, 2785.40),
        ("TSLA", 0.8, 248.20)
    ]

    print("🐦 Testing Twitter Message Generator:")
    print("-" * 50)
    
    # Test alert message
    alert_msg = create_stock_alert_message(test_data)
    print("📱 Stock Alert Message:")
    print(alert_msg)
    print()

    # test summary message
    summary_msg = create_market_summary(test_data)
    print("📊 Market Summary Message:")
    print(summary_msg)


if __name__ == "__main__":
    test_message_generator()