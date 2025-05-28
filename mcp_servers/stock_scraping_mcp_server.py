#!/usr/bin/env python3
import sys
import os

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#!/usr/bin/env python3
import asyncio
import json
import yfinance as yf
from mcp.server import Server
from mcp.types import Tool, TextContent
from datetime import datetime

app = Server("stock-scraping-mcp-server")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_stock_price",
            description="Get current stock price and data",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL)"}
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_multiple_stocks",
            description="Get data for multiple stocks",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbols": {"type": "array", "items": {"type": "string"}, "description": "List of stock symbols"}
                },
                "required": ["symbols"]
            }
        ),
        Tool(
            name="get_market_movers",
            description="Get top gaining and losing stocks",
            inputSchema={
                "type": "object",
                "properties": {
                    "market": {"type": "string", "description": "Market to analyze", "default": "US"}
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_stock_price":
        try:
            symbol = arguments["symbol"].upper()
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="2d")
            
            if hist.empty:
                return [TextContent(type="text", text=f"❌ No data found for {symbol}")]
            
            current_price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            change = current_price - prev_price
            change_pct = (change / prev_price) * 100
            
            result = {
                "symbol": symbol,
                "current_price": round(current_price, 2),
                "change": round(change, 2),
                "change_percent": round(change_pct, 2),
                "volume": info.get("volume", 0),
                "market_cap": info.get("marketCap", 0),
                "timestamp": datetime.now().isoformat()
            }
            
            return [TextContent(
                type="text",
                text=f"📊 {symbol}: ${result['current_price']} ({result['change']:+.2f}, {result['change_percent']:+.2f}%)\n{json.dumps(result, indent=2)}"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Error getting stock data: {str(e)}")]
    
    elif name == "get_multiple_stocks":
        try:
            symbols = [s.upper() for s in arguments["symbols"]]
            results = []
            
            for symbol in symbols:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                    change_pct = ((current_price - prev_price) / prev_price) * 100
                    
                    results.append({
                        "symbol": symbol,
                        "price": round(current_price, 2),
                        "change_percent": round(change_pct, 2)
                    })
            
            # Sort by performance
            results.sort(key=lambda x: x["change_percent"], reverse=True)
            
            return [TextContent(
                type="text",
                text=f"📊 Stock Performance Summary:\n{json.dumps(results, indent=2)}"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Error getting multiple stocks: {str(e)}")]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())


