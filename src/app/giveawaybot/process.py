# coding: utf-8
from pathlib import Path
from datetime import datetime
import json, os
from .detect import detect_giveaway
from .twitter import twitter as tw

RESULTS_DIR = Path(__file__).parent.parent.absolute() / "outputs"
SOURCES_DIR = Path(__file__).parent.parent.absolute() / "sources"


def create_historic_file(historic_file: str):
    if not os.path.isfile(RESULTS_DIR / historic_file):
        with open(RESULTS_DIR / historic_file, "w") as hist_file:
            json.dump({"tweets": []}, hist_file)
    return historic_file


def sort_by_post_time(record: dict):
    """sort a dict of tweets by post time

    Args:
        record (dict): dict of tweets

    Returns:
        list: sorted dict of tweets

    """
    # todo test this function
    {k: v for k, v in sorted(record.items(), key=lambda item: item["post_time"])}
    return sorted(dict, key=lambda tweet: tweet["post_time"])


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


def return_list_id_mentioned_users(mentioned_users: list):
    """return a list of mentioned users id from the list "mentionedUsers" contained in a tweet record

    Args:
        mentioned_users (list): list containing all of mentioned users

    Returns:
        list: id list of mentioned users
    """
    return [] if not mentioned_users else [user["id"] for user in mentioned_users]


def add_new_users_to_sources(list_new_users: list):
    """add new users to the sources filess

    Args:
        list_new_users (list): list of new users

    Returns:
        None: add new users to the sources files
    """
    with open(SOURCES_DIR / "sources.json", "r", encoding="utf-8") as sources_file:
        t = tw()
        sources_file_data = json.load(sources_file)
        already_in_sources = [user["account"] for user in sources_file_data["sources"]]
        for potential_user in list_new_users:
            name_potential_user = t.get_user_name_from_id(potential_user)
            if name_potential_user not in already_in_sources:
                sources_file_data["sources"].append({"account": name_potential_user})
    with open(RESULTS_DIR / "sources.json", "w", encoding="utf-8") as sources_file:
        json.dump(sources_file_data, sources_file)


#
# for user in list_new_users:
# if user not in sources:
# sources.append(user)
# return sources


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
            # do a function with hist_file as a parameter
            historic = json.load(hist_file)
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
            # do a function with r_file as a parameter
            new_record_to_process = 0
            all_new_mentionned_users = []
            for new_line_record in r_file:
                new_record = json.loads(new_line_record)
                is_giveaway = detect_giveaway(new_record["content"])
                if new_record["id"] not in list_current_id:
                    list_mentioned_users = return_list_id_mentioned_users(
                        new_record["mentionedUsers"]
                    )
                    [all_new_mentionned_users.append(u) for u in list_mentioned_users]
                    data = {
                        "accound_id": new_record["user"]["id"],
                        "tweet_id": new_record["id"],
                        "url": new_record["url"],
                        "post_time": new_record["date"],
                        "process_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "mentionned_accounts_id": list_mentioned_users,
                        "is_giveaway": is_giveaway,
                    }
                    status = take_part_in_giveaway_from_record(data)
                    data["status"] = status
                    data["overall_status"] = is_participation_complete(status)
                    historic["tweets"].append(data)
                    new_record_to_process += 1
                add_new_users_to_sources(all_new_mentionned_users)
            print(f"{new_record_to_process} new records have been processed")
    print("write historic file")
    with open(RESULTS_DIR / historic_file, "w") as new_hist_file:
        json.dump(historic, new_hist_file)


if __name__ == "__main__":
    # read_last_results("scrap_results.jsonl")
    update_tweet_lists("test_tweet.jsonl", "test_tweets_historic.json")
