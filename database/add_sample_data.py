import sqlite3
from datetime import datetime

def add_sample_stock():
    connection = sqlite3.connect("database/stock_mcp.db")
    cursor = connection.cursor()

    sample_data = [
        ("AAPL", 150.25, "2025-05-27 16:10:00"),
        ("GOOGL", 2800.50, "2025-05-27 16:10:00"),
        ("TSLA", 245.75, "2025-05-27 16:10:00")
    ]

    cursor.executemany(
        "INSERT INTO stock_data (symbol, price, timestamp) VALUES (?, ?, ?)",
        sample_data
    )

    print("✅ Sample stock data added!")
    print("📊 Added: AAPL, GOOGL, TSLA")

    connection.commit()
    connection.close()

if __name__ == "__main__":
    add_sample_stock()