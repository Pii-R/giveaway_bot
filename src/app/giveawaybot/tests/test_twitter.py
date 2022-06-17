from ..twitter import twitter
import json
from mock import patch, mock


class Tweet:
    def __init__(self, favorited):
        self.favorited = favorited


def test_is_already_liked(mocker):
    api = mocker.patch("tweepy.API")
    api.return_value.get_status.side_effect = (
        lambda x: Tweet(True) if x == "123456" else Tweet(False)
    )
    t = twitter()
    assert t.is_already_liked("123456")
    assert not t.is_already_liked("654321")


def test_follow_account(mocker):
    api = mocker.patch("tweepy.API")
    api.return_value.create_friendship("1").return_value = True
    t = twitter()
    assert t.follow_account("2") == {"success": True}


def test_return_tweet_by_id(mocker, shared_datadir, monkeypatch):
    def mockreturn():
        with open(shared_datadir / "tweet.json", "r", encoding="utf-8") as tweet:
            return json.load(tweet)

    t = twitter()

    monkeypatch.setattr(t, "get_tweet", mockreturn)
    t.get_tweet()["id"] == 1050118621198921728
