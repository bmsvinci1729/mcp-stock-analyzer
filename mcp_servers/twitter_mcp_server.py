#!/usr/bin/env python3
import sys
import os
import asyncio
import json
from mcp.server import Server
from mcp.types import Tool, TextContent
import tweepy

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Server("twitter-mcp-server")

def init_twitter_api():
    """Initialize Twitter API using environment variables"""
    
    # env credentials
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    
    # Initialize Twitter API v2 client
    client_v2 = tweepy.Client( # v1 expects tweepy.API... didn't wrk out for me, raising 403 forbidden error
        bearer_token=bearer_token,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
        wait_on_rate_limit=True
    )
    
    # auth setup OAuth
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api_v1 = tweepy.API(auth, wait_on_rate_limit=True) # v1 here
    
    return client_v2, api_v1

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="post_tweet",
            description="Post a tweet to Twitter",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Tweet content"},
                    "reply_to": {"type": "string", "description": "Tweet ID to reply to(not nececessary)"}
                },
                "required": ["text"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        client_v2, api_v1 = init_twitter_api()
        
        if name == "post_tweet":
            # Use API v2 for posting tweets v1.1 leads to permission errors sometimes
            response = client_v2.create_tweet(
                text=arguments["text"],
                in_reply_to_tweet_id=arguments.get("reply_to")
            )
            
            tweet_id = response.data['id']
            return [TextContent(
                type="text",
                text=f"Tweet posted successfully! ID: {tweet_id}"
            )]
            
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
