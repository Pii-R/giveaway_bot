from ..process import complete_old_tweets


def test_complete_old_tweets_with_one_tweet(shared_datadir):
    with open(
        shared_datadir / "historic_results_test.json", "r", encoding="utf-8"
    ) as historic_results_file:
        assert complete_old_tweets(historic_results_file) == [
            1531329340826210306,
            1531213837722169344,
            1531166014334980096,
        ]
