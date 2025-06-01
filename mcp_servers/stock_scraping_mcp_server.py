#!/usr/bin/env python3
import sys
import os
import asyncio
import json
import yfinance as yf
from mcp.server import Server
from mcp.types import Tool, TextContent
from datetime import datetime

# Add project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Server("stock-scraping-mcp-server")

@app.list_tools()
async def list_tools():
    # Register available tools for this MCP server
    return [
        Tool(
            name="get_multiple_stocks",
            description="Get detailed data for multiple stocks",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbols": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of stock symbols"
                    }
                },
                "required": ["symbols"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_multiple_stocks":
        try:
            symbols = [s.upper() for s in arguments["symbols"]]
            results = []
            for symbol in symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="2d")
                    info = ticker.info if hasattr(ticker, 'info') and ticker.info else {}
                    # Only add if price data is available
                    if hist is not None and not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                        change = current_price - prev_price
                        change_pct = (change / prev_price) * 100 if prev_price else 0
                        results.append({
                            "symbol": symbol,
                            "current_price": round(current_price, 2),
                            "change": round(change, 2),
                            "change_percent": round(change_pct, 2),
                            "volume": info.get("volume", 0),
                            "market_cap": info.get("marketCap", 0),
                            "timestamp": datetime.now().isoformat()
                        })
                except Exception as stock_e:
                    # Log error for this symbol
                    results.append({
                        "symbol": symbol,
                        "error": str(stock_e)
                    })
            # Sort by percent change, descending
            results.sort(key=lambda x: x.get("change_percent", 0), reverse=True)
            return [TextContent(
                type="text",
                text=f"Stock Performance Summary:\n{json.dumps(results, indent=2)}"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting multiple stocks: {str(e)}")]

async def main():
    from mcp.server.stdio import stdio_server
    # Start the MCP server using stdio
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())

