from twitter import twitter
from detect import detect_giveaway
class giveAwayBot():
   def __init__(self):
      self.t = twitter()
      
   def analyze_home_timeline(self):
      tweet_list = self.t.get_tweets_from_home_timeline()
      for tweet in tweet_list:
         if detect_giveaway(tweet):
            print(detect_giveaway(tweet),tweet) 
      
if __name__ == "__main__":
   bot = giveAwayBot()
   bot.analyze_home_timeline()