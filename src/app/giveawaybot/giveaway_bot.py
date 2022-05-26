from .twitter import twitter
from .detect import detect_giveaway
from app.scraping.scrap import run_scraping
from .process import update_tweet_lists

class giveAwayBot():
   def __init__(self):
      self.t = twitter()
      
   def analyze_home_timeline(self):
      tweet_list = self.t.get_tweets_from_home_timeline()
      for tweet in tweet_list:
         if detect_giveaway(tweet):
            print(detect_giveaway(tweet),tweet) 
            
   def run_bot(self):
      ## get latest tweets
      scraping_params = {
         "search": "#concours",
         "class_search": "twitter-search",
         "max_results": 50,
         "start_time":"2022-05-22"
      }
      run_scraping(scraping_params)
      ## process them to know if they are new
      update_tweet_lists("test_tweet.jsonl","test_historic_results.json")
      ## if so apply rt, like and follow to take part in giveaway
      pass
      
if __name__ == "__main__":
   bot = giveAwayBot()
   bot.run_bot()
   # bot.analyze_home_timeline()