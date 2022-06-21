from app.scraping.scrap import run_scraping
from app.giveawaybot.process import update_tweet_lists
from pathlib import Path
import datetime, os

RESULTS_DIR = Path(__file__).parent.parent.absolute() / "outputs"


class giveAwayBot:
    def __init__(self):
        pass

    def create_empty_scrap_results_file(self):
        with open(RESULTS_DIR / "scrap_results.jsonl", "w") as scrap_results_file:
            pass

    def delete_old_scrap_results_file(self, file_path: str):
        if os.path.isfile(file_path):
            os.remove(file_path)

    def run_bot(self):
        self.delete_old_scrap_results_file(RESULTS_DIR / "global_scrap_results.jsonl")
        start_time = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime(
            "%Y-%m-%d"
        )
        scraping_params = {
            "search": "(concours)",
            "class_search": "twitter-search",
            "max_results": 50,
            "start_time": start_time,
        }
        if scraping_params["max_results"] > 0:
            run_scraping(scraping_params)
        else:
            self.create_empty_scrap_results_file()
        update_tweet_lists("global_scrap_results.jsonl", "historic_results.json")


if __name__ == "__main__":
    bot = giveAwayBot()
    bot.run_bot()
