# coding: utf-8
from pathlib import Path
from datetime import datetime
import json, os
from .detect import detect_giveaway
from .twitter import twitter as tw

RESULTS_DIR = Path(__file__).parent.parent.absolute() / "outputs"


def create_historic_file(historic_file: str):
    if not os.path.isfile(RESULTS_DIR / historic_file):
        with open(RESULTS_DIR / historic_file, "w") as hist_file:
            json.dump({"tweets": []}, hist_file)
    return historic_file


def read_last_results(result_file: str):
    result_file_path = RESULTS_DIR / result_file
    with open(result_file_path, "r", encoding="utf-8") as r_file:
        for record in r_file:
            print(record)


def is_participation_complete(status: dict):
    """return True if participation is complete else False

    Args:
        tweet_record (dict): tweet record

    Returns:
        bool: True if participation is complete else False
    """
    for followed_account in status["follow"]:
        for key_followed_account, value_followed_account in followed_account.items():
            if not value_followed_account["success"]:
                return False
    for liked_tweet in status["like"]:
        for key_liked_tweet, value_liked_tweet in liked_tweet.items():
            if not value_liked_tweet["success"]:
                return False
    for retweeted_tweet in status["rt"]:
        for key_retweeted_tweet, value_retweeted_tweet in retweeted_tweet.items():
            if not value_retweeted_tweet["success"]:
                return False
    return True


def take_part_in_giveaway_from_record(tweet_record: dict):
    """apply all actions to take part in a giveaway from a tweet record
    record : {"accound_id":new_record["user"]["id"],
                        "tweet_id":new_record["id"],
                        "url": new_record["url"],
                        "post_time": new_record["date"],
                        "process_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "mentionned_accounts_id": return_list_mentioned_users(new_record["mentionedUsers"]),
                        "is_giveaway": is_giveaway,
                        "status":"not completed"}

    Args:
        tweet_record (dict): _description_
    """
    my_tw = tw()
    accounts_to_follow = tweet_record["mentionned_accounts_id"] + [
        tweet_record["accound_id"]
    ]
    status = {"follow": [], "like": [], "rt": []}
    for account_id in accounts_to_follow:
        my_tw.follow_account(account_id)
        status["follow"].append({account_id: my_tw.follow_account(account_id)})

    my_tw.like_tweet(tweet_record["tweet_id"])
    status["like"].append(
        {tweet_record["tweet_id"]: my_tw.like_tweet(tweet_record["tweet_id"])}
    )
    my_tw.retweet(tweet_record["tweet_id"])
    status["rt"].append(
        {tweet_record["tweet_id"]: my_tw.retweet(tweet_record["tweet_id"])}
    )
    return status


def return_list_mentioned_users(mentioned_users: list):
    """return a list of mentioned users id from the list "mentionedUsers"

    Args:
        mentioned_users (list): list containing all of mentioned users

    Returns:
        list: id list of mentioned users
    """
    list_mentioned_users = []
    if mentioned_users:
        list_mentioned_users = [user["id"] for user in mentioned_users]
    return list_mentioned_users


def update_tweet_lists(scrap_result_file: str, historic_file: str):
    """update tweet lists from scrap result file and historic file
    one part of this function is to update the historic file and search for new tweets

    Args:
        scrap_result_file (str): _description_
        historic_file (str): _description_
    """
    historic_file = create_historic_file(historic_file)
    list_current_id = []
    with open(RESULTS_DIR / historic_file, "r+") as hist_file:
        with open(RESULTS_DIR / scrap_result_file, "r") as r_file:
            historic = json.load(hist_file)
            print(len(historic["tweets"]))
            print("check if tweet is already in historic file")
            historic_record_to_update = 0
            for historic_record in historic["tweets"]:
                list_current_id.append(historic_record["tweet_id"])
                if not historic_record["overall_status"]:
                    print(f"{historic_record['tweet_id']} is not completed")
                    status = take_part_in_giveaway_from_record(historic_record)
                    historic_record["status"] = status
                    historic_record["overall_status"] = is_participation_complete(
                        status
                    )
                    historic_record_to_update += 1
            print(f"{historic_record_to_update} records have been updated")
            print("process new tweets")
            new_record_to_process = 0
            for new_record in r_file:
                new_record = json.loads(new_record)
                is_giveaway = detect_giveaway(new_record["content"])
                if new_record["id"] not in list_current_id:
                    data = {
                        "accound_id": new_record["user"]["id"],
                        "tweet_id": new_record["id"],
                        "url": new_record["url"],
                        "post_time": new_record["date"],
                        "process_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "mentionned_accounts_id": return_list_mentioned_users(
                            new_record["mentionedUsers"]
                        ),
                        "is_giveaway": is_giveaway,
                    }
                    status = take_part_in_giveaway_from_record(data)
                    data["status"] = status
                    data["overall_status"] = is_participation_complete(status)
                    historic["tweets"].append(data)
                    new_record_to_process += 1
            print(f"{new_record_to_process} new records have been processed")
    print("write historic file")
    with open(RESULTS_DIR / historic_file, "w") as new_hist_file:
        json.dump(historic, new_hist_file)


if __name__ == "__main__":
    # read_last_results("scrap_results.jsonl")
    update_tweet_lists("test_tweet.jsonl", "test_tweets_historic.json")
