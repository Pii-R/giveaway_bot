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

    def is_already_retweeted(self, tweet_id: int) -> bool:
        """Checks if the tweet is already retweeted

        Args:
            tweet_id (int): id of the tweet

        Returns:
            bool: True if the tweet is already retweeted else False
        """
        return self.api.get_status(tweet_id).retweeted

    def is_already_liked(self, tweet_id: int) -> bool:
        """Checks if the tweet is already liked

        Args:
            tweet_id (int): id of the tweet

        Returns:
            bool: True if the tweet is already liked else False
        """
        return self.api.get_status(tweet_id).favorited

    def follow_account(self, account_id: int):
        """Follows an account with the given id
        Args:
            account_id (int): id of the account
        """
        success_response = {"success": True}
        fail_response = {"success": False}
        try:
            if not self.is_already_followed(account_id):
                self.api.create_friendship(user_id=account_id)
                return success_response
            return success_response
        except Forbidden as e:
            return fail_response

    def retweet(self, tweet_id: int):
        """Retweets a tweet with the given id

        Args:
            tweet_id (int): id of the tweet
        """
        success_response = {"success": True}
        fail_response = {"success": False}
        try:
            if not self.is_already_retweeted(tweet_id):
                self.api.retweet(tweet_id)
                return success_response
            self.api.retweet(tweet_id)
            return success_response
        except Forbidden as e:
            if "already retweeted" in str(e):
                return success_response
            return fail_response

    def like_tweet(self, tweet_id: int):
        """Likes a tweet with the given id
        Args:
            tweet_id (int): id of the tweet
        """
        success_response = {"success": True}
        fail_response = {"success": False}
        try:
            self.api.create_favorite(tweet_id)
            return success_response
        except Forbidden as e:
            if "already favorited" in str(e):
                return success_response
            return fail_response


if __name__ == "__main__":
    t = twitter()
    # t.follow_account(1225440114832281600)
    # t.like_tweet(1529401913602625536)
    # t.retweet(1529401913602625536)
    # print(t.follow_account(1537646028))
    print(t.is_already_liked(1529401913602625536))
    # print(t.follow_account(1537646028))

    # print(t.api.last_response.status_code)
    # int(t.api.getheader('x-rate-limit-limit'))
    # print(t.get_tweet_by_id(1512445562167169029))
