# coding: utf-8
"fonctions used for analyzing tweet and return what kind of message there is inside"
from .twitter import twitter
from .utils import remove_emoji
from nltk.tokenize import word_tokenize

def detect_giveaway(tweet:str)->bool:
    """use this fonction to determine if a tweet is about a giveaway or not
    Args:
        tweet (str): tweet text to analyze
    Returns:
        bool: True if tweet talks about giveaway False if not
    """    
    giveaway_words_list = ["participer","concours","gagner","gagnant"]
    format_tweet = remove_emoji(tweet.lower())
    tokenized_format_tweet = word_tokenize(format_tweet)
    l=[char in giveaway_words_list for char in tokenized_format_tweet]
    if True in l :
        return True
    return False


if __name__ == "__main__":
    t = twitter()
    tweet_example = t.get_tweet_by_id(1512445562167169029)
    print(detect_giveaway(tweet_example))