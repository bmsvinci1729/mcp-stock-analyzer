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
    
    # Get credentials from environment variables
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    
    # Validate that all required credentials are present
    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        raise ValueError("Missing required Twitter API credentials in .env file")
    
    # Initialize Twitter API v2 client
    client_v2 = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
        wait_on_rate_limit=True
    )
    
    # Initialize v1.1 API for legacy endpoints
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api_v1 = tweepy.API(auth, wait_on_rate_limit=True)
    
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
                    "reply_to": {"type": "string", "description": "Tweet ID to reply to (optional)"}
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="search_tweets",
            description="Search for tweets by keyword or hashtag",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "count": {"type": "integer", "description": "Number of tweets", "default": 10}
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        client_v2, api_v1 = init_twitter_api()
        
        if name == "post_tweet":
            # Use API v2 for posting tweets
            response = client_v2.create_tweet(
                text=arguments["text"],
                in_reply_to_tweet_id=arguments.get("reply_to")
            )
            
            tweet_id = response.data['id']
            return [TextContent(
                type="text",
                text=f"✅ Tweet posted successfully! ID: {tweet_id}"
            )]
            
        elif name == "search_tweets":
            # Use API v2 for searching tweets
            tweets = client_v2.search_recent_tweets(
                query=arguments["query"],
                max_results=min(arguments.get("count", 10), 100),
                tweet_fields=["created_at", "author_id", "public_metrics"]
            )
            
            results = []
            if tweets.data:
                for tweet in tweets.data:
                    results.append({
                        "id": tweet.id,
                        "text": tweet.text,
                        "author_id": tweet.author_id,
                        "created_at": str(tweet.created_at),
                        "retweets": tweet.public_metrics.get("retweet_count", 0),
                        "likes": tweet.public_metrics.get("like_count", 0)
                    })
            
            return [TextContent(
                type="text",
                text=f"Found {len(results)} tweets: {json.dumps(results, indent=2)}"
            )]
            
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
