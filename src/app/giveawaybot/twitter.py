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
        """Gets a tweet by id

        Args:
            id (int): id of the tweet

        Returns:
            str: tweet
        """        
        return self.api.get_status(id=id, tweet_mode="extended").full_text
    
    def follow_account(self,account_id: int):
        """Follows an account with the given id
        Args:
            account_id (int): id of the account
        """        
        self.api.create_friendship(user_id = account_id)

    def retweet(self,tweet_id:int):
        """Retweets a tweet with the given id

        Args:
            tweet_id (int): id of the tweet
        """        
        self.api.retweet(tweet_id)

    def like_tweet(self,tweet_id:int):
        self.api.create_favorite(tweet_id)
        pass
    
if __name__ == "__main__":
    t = twitter()
    t.follow_account(898994539)
    t.like_tweet(1529401913602625536)
    t.retweet(1529401913602625536)
    # print(t.get_tweet_by_id(1512445562167169029))