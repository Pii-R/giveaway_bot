from .twitter import twitter
from app.scraping.scrap import run_scraping
from .process import update_tweet_lists
from pathlib import Path
import datetime

RESULTS_DIR = Path(__file__).parent.parent.absolute() / "outputs"


class giveAwayBot:
    def __init__(self):
        pass

    def create_empty_scrap_results_file(self):
        with open(RESULTS_DIR / "scrap_results.jsonl", "w") as scrap_results_file:
            pass

    def run_bot(self):
        ## get latest tweets
        start_time = "2022-05-30"
        # datetime.datetime.now()
        scraping_params = {
            "search": "#concours",
            "class_search": "twitter-search",
            "max_results": 10,
            "start_time": start_time,
        }
        if scraping_params["max_results"] > 0:
            run_scraping(scraping_params)
        else:
            self.create_empty_scrap_results_file()
        # update_tweet_lists("test_tweet.jsonl","test_historic_results.json")
        update_tweet_lists("scrap_results.jsonl", "historic_results.json")


if __name__ == "__main__":
    bot = giveAwayBot()
    bot.run_bot()
