# MCP - Stock Analyzer


Model Context Protocol (MCP) server system for real-time stock market datat scraping, storage and retrieval, analysis, and automated social media posting. 
Three specialized MCP servers that enable AI agents to collect, store and extract stock data, analyze market performance from yfinance, and post impressive market updates to X (Twitter)

## Disclaimer
This project is for educational and research purposes only. Not financial advice. Use at your own risk when making investment decisions.😅

## The project:
A demonstration of building MCP servers that integrate with Agents like Claude Desktop and VS Code (MCP Client). System's major 3 components:
1. Stock Scraping server: Real time stock data fetched from Yahoo Finance
2. Database server: Fetched data stored, retrieved, and analyzed using SQLite3.
3. X(Twitter) server: The analyzed data is curated into an impressive post and automatically posted as market updates on X (Twitter) usign X APIs
## So how does this work ? 🤔 

The MCP allows the MCP Clients to use external tools. MCP servers described above shall expose the required tools that the AI/Client can call when in need.
1. Ask LLMs : "Get current price of Apple stock, and tweet about it" - very simple prompt.
2. Now, Claude shall call :
   - stock scraper tool to get Apple's current price
   - database tool to store the data, and retrieve
   - twitter tool to post a tweet with the information 

The servers integrated into the AI now, the dropdown reveals the tools associated with them 
![Screenshot from 2025-06-01 12-52-24](https://github.com/user-attachments/assets/a7af09dd-fe47-41b8-ad91-912f3bee516a)


<br />
The twitter post:<br />

![Screenshot from 2025-06-01 16-01-55](https://github.com/user-attachments/assets/70e1609e-7515-43d6-8f0b-8e98070735bb)



## Setup
### Prerequisites
  - Python 3.10 or higher
  - Twitter Developer Account with API access (Basic tier required for posting) **Consumer API key and secret**, and **Access token and secret**
  - Claude Desktop or VS Code with MCP support (I have used these, there other clients out there, room for exploration)

### Installation
  - Clone and setup
    ```
    git clone https://github.com/bmsvinci1729/mcp-stock-analyzer.git
    cd mcp-stock-analyzer

    # Create virtual environment
    python3 -m venv stock-mcp
    source stock-mcp/bin/activate  # On Windows: stock-mcp\Scripts\activate
    
    # Install dependencies
    pip install mcp yfinance tweepy python-dotenv asyncio
    Well its age of "uv" too!!

    ```
  - Configure your Environment variables
    Create a ```.env``` file in the project root:
    ```
    # Twitter API Credentials
    TWITTER_CONSUMER_KEY=your_consumer_key_here
    TWITTER_CONSUMER_SECRET=your_consumer_secret_here
    TWITTER_ACCESS_TOKEN=your_access_token_here
    TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
    TWITTER_BEARER_TOKEN=your_bearer_token_here
    
    # Database Configuration
    DATABASE_PATH=/path/to/your/project/database/stocks.db

    ```
    Caution: Don't commit this file to your github, if you are experimenting or modifying further

  - Now a configuration for our Agents/Clients, here is the ```claude_desktop_config.json```: Claude Desktop -> File -> Settings -> Developer -> Edit config
    ```
    {
      "mcpServers": {
        "stock-scraping": {
          "command": "/path/to/your/project/stock-mcp/bin/python",
          "args": ["/path/to/your/project/stock_scraping_mcp_server.py"]
        },
        "stock-database": {
          "command": "/path/to/your/project/stock-mcp/bin/python",
          "args": ["/path/to/your/project/database_server.py"]
        },
        "stock-twitter": {
          "command": "/path/to/your/project/stock-mcp/bin/python",
          "args": ["/path/to/your/project/twitter_mcp_server.py"]
        }
      }
    }

    ```

  - Begin your experiments (interacting):
  ```
`    "Get prices for Apple, Google, Tesla and Microsoft"
  ```
  ```
    "Store the current NVIDIA stock price in the database"
    "Show me Apple stock data from the last hour"
    "Get the top 5 performing stocks from today"
    "Post a tweet about the current market performance"
  ```
  ```
    "Analyze the top 10 tech stocks, identify the biggest movers, and post a professional market update tweet"
  ```

## Learn more and dive deeper (resources)
- [MCP](https://modelcontextprotocol.io/introduction)
- MCP [lecture](https://www.youtube.com/watch?v=kQmXtrmQ5Zg&pp=ygUVbWNwIGxlY3R1cmUgYW50aHJvcGlj) by Anthropic
- [X API](https://developer.x.com/en/docs/x-api)
- [Claude Desktop for Linux](https://github.com/aaddrick/claude-desktop-debian) - Calmly do follow the instructions
- I did get several issues related to X API's 403 Forbidden error, do ensure token_ids and secrets are correct, sometimes a rate-limit issue.
