import sys
import os
import time
from datetime import datetime

sys.path.append('database')
sys.path.append('scrapers')
sys.path.append('twitter')

from scrapers.auto_updater import update_all_stocks
from database.perf_analyzer import find_top_performer
from twitter.message_generator import create_stock_alert_message
from twitter.twitter_poster import TwitterPoster
from datetime import datetime

def run_15_minute_cycle_with_posting():
    print(f"📊 {datetime.now().strftime('%H:%M:%S')} - Running 15-minute analysis...")
    twitter = TwitterPoster()
    performace_data = find_top_performer()
    if performace_data:
        sorted_performance = sorted(performace_data, key = lambda x:x[1], reverse = True)

        message = create_stock_alert_message(sorted_performance)
        print("Twitter message generated")
        print("-" * 50)
        print(message)
        print("-" * 50)
        success = twitter.post_tweet(message)

        if success:
            print("✅ Tweet posted successfully!")
        else:
            print("❌ Tweet posting failed")
        
        # Still save to file as backup
        with open("generated_tweets.txt", "a") as f:
            f.write(f"\n{datetime.now()}\n{message}\n{'='*50}\n")
    
    print("✅ Analysis and posting complete!")

def run_5_minute_cycle():
    print(f"🔄 {datetime.now().strftime('%H:%M:%S')} - Running 5-minute update...")
    update_all_stocks()
    print("✅ Stock prices updated!")

def run_15_minute_cycle():
    print(f"📊 {datetime.now().strftime('%H:%M:%S')} - Running 15-minute analysis...")
    performance_data = find_top_performer()

    if performance_data:
        # Sort by performance (best first)
        sorted_performance = sorted(performance_data, key=lambda x: x[1], reverse=True)
    
        message = create_stock_alert_message(sorted_performance)
        
        print("\n🐦 Generated Twitter Message:")
        print("-" * 50)
        print(message)
        print("-" * 50)
        
        # Save message to file for now (later we'll post to Twitter)
        with open("generated_tweets.txt", "a") as f:
            f.write(f"\n{datetime.now()}\n{message}\n{'='*50}\n")
        
        print("💾 Message saved to generated_tweets.txt")
    
    print("✅ Analysis complete!")

def main_loop():
    print("🚀 Starting Stock MCP Automation System!")
    print("⏰ Will update prices every 5 minutes")
    print("📊 Will analyze and post every 15 minutes")
    print("Press Ctrl+C to stop\n")

    time.sleep(1)

    cycle_count = 0

    try:
        while True:
            cycle_count += 1

            run_5_minute_cycle()
            if cycle_count % 3 == 0:
                run_15_minute_cycle()

            print(f"😴 Sleeping for 5 minutes... (Cycle {cycle_count})")
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n🛑 System stopped by user")
        print("📊 Check generated_tweets.txt for all messages!")


if __name__ == "__main__":
    print("Testing twitter integration BOOOOM")

    run_15_minute_cycle_with_posting()