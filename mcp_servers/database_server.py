"""
    Standard MCP server functions:
        1. list tools - each tool shall have a name, a description, and inputSchema(like a function input)
        2. call tool - call each tool with required inputs, and define (just the way we define a declared function) each tool using try catch blocks
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio # for concurrent execution
import sqlite3
from datetime import datetime, timedelta
from mcp.server import Server # Server is the class under mcp module's server module
# are package and module same ? Answer: No, a package is a collection of modules, while a module is a single file containing Python code.
from mcp.types import Tool, TextContent
import json

# Initialize MCP Server
app = Server("stock-database-server")
# handles incoming requests and manages tools for stock data operations

# Get absolute path to database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "stocks.db")

@app.list_tools()
# what exactly is the above line meaning ? Answer: It is a decorator that registers the function `list_tools` as a tool listing function for the MCP server.
async def list_tools(): # why async? answer: To allow concurrent execution and non-blocking I/O operations, which is useful for handling multiple requests efficiently.
    """List available database tools"""
    return [
        Tool(
            name="fetch_stock_data",
            description="Fetch stock data from database with filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (optional)"},
                    "timeframe_minutes": {"type": "integer", "description": "Minutes back to fetch", "default": 2}
                }
            }
        ),
        Tool(
            name="get_top_performers",
            description="Get top performing stocks",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of top stocks", "default": 2},
                    "timeframe_minutes": {"type": "integer", "description": "Analysis timeframe", "default": 3}
                }
            }
        ),
        Tool(
            name="store_stock_data",
            description="Store new stock data in database",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol"},
                    "price": {"type": "number", "description": "Current price"},
                    "volume": {"type": "integer", "description": "Trading volume"},
                    "market_cap": {"type": "integer", "description": "Market cap"},
                    "pe_ratio": {"type": "number", "description": "P/E ratio"}
                },
                "required": ["symbol", "price"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    # why do we have some argumenrts like name and arguments in this function an dwhy not in the previous funciton fetch_stock_data?
    # answer to above question: The `call_tool` function is designed to handle tool calls dynamically based on the tool name and its arguments, 
    # allowing for flexible execution of different database operations. 
    # In contrast, `fetch_stock_data` is a specific tool that fetches stock data and has its own parameters defined in the tool schema.
    """Handle tool calls"""
    
    if name == "fetch_stock_data":
        symbol = arguments.get("symbol")
        timeframe = arguments.get("timeframe_minutes", 60)
        
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            
            cutoff_time = datetime.now() - timedelta(minutes=timeframe)
            cutoff_str = cutoff_time.strftime("%Y-%m-%d %H:%M:%S")
            
            if symbol:
                cursor.execute("""
                    SELECT * FROM real_stock_data 
                    WHERE symbol = ? AND timestamp >= ?
                    ORDER BY timestamp DESC
                """, (symbol, cutoff_str))
            else:
                cursor.execute("""
                    SELECT * FROM real_stock_data 
                    WHERE timestamp >= ?
                    ORDER BY timestamp DESC
                """, (cutoff_str,))
            
            results = cursor.fetchall()
            connection.close()
            
            return [TextContent(
                type="text",
                text=f"Found {len(results)} records: {json.dumps([dict(zip(['id', 'symbol', 'price', 'volume', 'market_cap', 'pe_ratio', 'timestamp'], row)) for row in results[:10]])}"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Database error: {str(e)}")]
    
    elif name == "get_top_performers":
        limit = arguments.get("limit", 5)
        timeframe = arguments.get("timeframe_minutes", 15)
        
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            
            # Simple top performers query without external import
            cutoff_time = datetime.now() - timedelta(minutes=timeframe)
            cutoff_str = cutoff_time.strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute("""
                SELECT symbol, 
                       AVG(price) as avg_price,
                       COUNT(*) as data_points,
                       MAX(timestamp) as latest_time
                FROM real_stock_data 
                WHERE timestamp >= ?
                GROUP BY symbol
                ORDER BY avg_price DESC
                LIMIT ?
            """, (cutoff_str, limit))
            
            results = cursor.fetchall()
            connection.close()
            
            performers = []
            for row in results:
                performers.append({
                    "symbol": row[0],
                    "avg_price": round(row[1], 2),
                    "data_points": row[2],
                    "latest_time": row[3]
                })
            
            return [TextContent(
                type="text",
                text=f"Top {len(performers)} performers: {json.dumps(performers, indent=2)}"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Performance analysis error: {str(e)}")]
    
    elif name == "store_stock_data":
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            
            # Create table if it doesn't exist
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
            
            cursor.execute('''
                INSERT INTO real_stock_data 
                (symbol, price, volume, market_cap, pe_ratio, timestamp) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                arguments["symbol"],
                arguments["price"],
                arguments.get("volume", 0),
                arguments.get("market_cap", 0),
                arguments.get("pe_ratio", 0),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            
            connection.commit()
            connection.close()
            
            return [TextContent(
                type="text",
                text=f"Stored data for {arguments['symbol']} at ${arguments['price']}"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Storage error: {str(e)}")]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
