import sqlite3

def view_all_stocks():
    connection = sqlite3.connect("database/stock_mcp.db")
    cursor = connection.cursor()

    #getting all stocks
    cursor.execute("SELECT * FROM stock_data")  # stock_data is the table name stock_mcp is the database name
    all_data = cursor.fetchall()

    # use of fetchall() to get all the data from the table
    print("Current stock data:")
    for row in all_data:
        stock_id, symbol, price, timestamp = row
        print(f"🏷️  {symbol}: ${price} at {timestamp}")
    
    connection.close()

def find_highest_price():
    connection = sqlite3.connect("database/stock_mcp.db")
    cursor = connection.cursor()

    cursor.execute("SELECT symbol, price from stock_data order by price desc limit 1")
    result = cursor.fetchone()

    if result:
        symbol, price = result
        print(f"Life is BULLY at: {symbol} price: ${price}")

    connection.close()

if __name__ == "__main__":
    view_all_stocks()
    print()
    find_highest_price()