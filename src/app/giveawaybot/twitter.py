import tweepy
from tweepy.errors import Forbidden
import os

API_KEY = os.environ.get("API_KEY")
API_KEY_SECRET = os.environ.get("API_KEY_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")


class twitter:
    MY_ID = 188690550

    def __init__(self):
        self.auth = tweepy.OAuth1UserHandler(
            API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
        )
        self.api = tweepy.API(self.auth)

    def get_tweets_from_home_timeline(self):
        public_tweets = self.api.home_timeline(count=200, tweet_mode="extended")
        return [tweet.full_text for tweet in public_tweets]

    def get_tweet_by_id(self, id: int):
        """Gets a tweet by id

        Args:
            id (int): id of the tweet

        Returns:
            str: tweet
        """
        return self.api.get_status(id=id, tweet_mode="extended").full_text

    def is_already_followed(self, account_id: int) -> bool:
        """check if the account is already followed

        Args:
            account_id (int): id of the account to check

        Returns:
            bool: True if the account is already followed else False
        """
        fs = self.api.get_friendship(source_id=self.MY_ID, target_id=account_id)
        return fs[0].following

    def follow_account(self, account_id: int):
        """Follows an account with the given id
        Args:
            account_id (int): id of the account
        """
        try:
            if not self.is_already_followed(account_id):
                self.api.create_friendship(user_id=account_id)
                return {"success": True}
            return {"success": True}
        except Forbidden as e:
            return {"success": False}

    def retweet(self, tweet_id: int):
        """Retweets a tweet with the given id

        Args:
            tweet_id (int): id of the tweet
        """
        try:
            self.api.retweet(tweet_id)
            return {"success": True}
        except Forbidden as e:
            if "already retweeted" in str(e):
                return {"success": True}
            return {"success": False}

    def like_tweet(self, tweet_id: int):
        try:
            self.api.create_favorite(tweet_id)
            return {"success": True}
        except Forbidden as e:
            if "already favorited" in str(e):
                return {"success": True}
            return {"success": False}


if __name__ == "__main__":
    t = twitter()
    # t.follow_account(1225440114832281600)
    # t.like_tweet(1529401913602625536)
    # t.retweet(1529401913602625536)
    # print(t.follow_account(1537646028))
    print(t.follow_account(1537646028))

    # print(t.api.last_response.status_code)
    # int(t.api.getheader('x-rate-limit-limit'))
    # print(t.get_tweet_by_id(1512445562167169029))
