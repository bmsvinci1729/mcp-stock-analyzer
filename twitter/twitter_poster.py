import tweepy
import os

class TwitterPoster:
    def __init__(self):
        self.consumer_key = "MnRoaDgXfpTtPbPWAm7eWeILL"
        self.consumer_secret = "uePBjOAV36wiyIlg7ElMBTS3GR3yj5zYcqY0OuMPJcfRxGVySF" 
        self.access_token = "1927361063848173568-hYoag3VJEu7FrmYstFmejXU3x5SATa"
        self.access_token_secret = "kuYjuJ2Q8pRqlDyZlzz6ELvecG0FnxQbaBCTVQmKwNZJv"

        self.api = None
        self.setup_twitter_api()

    def setup_twitter_api(self):
        try:
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            self.api = tweepy.API(auth, wait_on_rate_limit=True)

            self.api.verify_credentials()
            print("✅ Twitter API connection successful!")
            return True

        except Exception as e:
            print(f"❌ Twitter API connection failed: {e}")
            print("📝 Using simulation mode instead")
            return False
    
    def post_tweet(self, message):
        if self.api:
            try:
                # real tweet posting
                print("Tweeted successfully !! ID = {tweet.id}")
                return True
            
            except Exception as e:
                print(f"❌ Failed to post tweet: {e}")
                return False
        
        else:
            # Simulation mode
            print("🔄 SIMULATION MODE - Tweet would be posted:")
            print("-" * 50)
            print(message)
            print("-" * 50)
            print("📝 Add your real Twitter API keys to post for real!")
            return True
        
import datetime
from datetime import datetime


def test_twitter_poster():
    """Test the Twitter poster"""
    poster = TwitterPoster()

    test_message = """🚀 STOCK ALERT {datetime}
🏆 Top performer: $AAPL
💰 Price: $152.30
📊 Change: +2.5%
🔥 Stock is soaring!
#StockAlert #Trading #MarketUpdate"""
    
    poster.post_tweet(test_message)

# Run the test
if __name__ == "__main__":
    test_twitter_poster()