from ..twitter import twitter
import json
from mock import patch, mock


# def mocked_tweet(tweet_id):
#     if tweet_id == 1:
#         return True
#     else:
#         return False
def mocked_foo(*args, **kwargs):
    print("coucou0")

    if kwargs.get("tweet_id") == 1:
        return 0
    else:
        return 1


@patch("tweepy.API.get_status")
def test_is_already_liked(mocker):
    mock.side_effect = mocked_foo
    t = twitter()
    print(t.is_already_liked(1))
    assert t.is_already_liked(1) == True


# def test_is_already_liked(mocker):
#     t = twitter()
#     t.is_already_liked(1234).return_value.favorited = True
#     assert t.is_already_liked(14)


def test_follow_account(mocker):
    api = mocker.patch("tweepy.API")
    api.return_value.create_friendship("1").return_value = True
    t = twitter()
    assert t.follow_account("2") == {"success": True}


def test_return_tweet_by_id(mocker, shared_datadir, monkeypatch):
    t = twitter()

    def mockreturn():
        with open(shared_datadir / "tweet.json", "r", encoding="utf-8") as tweet:
            return json.load(tweet)

    monkeypatch.setattr(t, "get_tweet", mockreturn)
    t.get_tweet()["id"] == 1050118621198921728

    # api = mocker.patch("tweepy.API")
    # api.return_value.get_status.return_value.full_text = "tweet"
    # t = twitter()
    # assert t.get_tweet_by_id("123456") == "tweet"
