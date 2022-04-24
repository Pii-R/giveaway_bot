from itertools import count
import tweepy
import os

API_KEY = os.environ.get("API_KEY")
API_KEY_SECRET = os.environ.get("API_KEY_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

class twitter():
    def __init__(self):
        self.auth = tweepy.OAuth1UserHandler(
        API_KEY, API_KEY_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)


    def get_tweets_from_home_timeline(self):
        public_tweets = self.api.home_timeline(count = 200, tweet_mode="extended" )
        return [tweet.full_text for tweet in public_tweets]


    def get_tweet_by_id(self, id:int):
        return self.api.get_status(id=id, tweet_mode="extended").full_text
    
if __name__ == "__main__":
    t = twitter()
    print(t.get_tweet_by_id(1512445562167169029))