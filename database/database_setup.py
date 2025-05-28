import sqlite3
import os

def create_database():
    db_path = "database/stock_mcp.db" # different from the original

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_data (
            id INTEGER PRIMARY KEY,
            symbol TEXT NOT NULL,
            price REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    print("✅ Database created successfully!")
    print(f"📁 Database location: {db_path}")   

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_database()