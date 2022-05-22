#coding: utf-8
from pathlib import Path
from datetime import datetime
import json
from .detect import detect_giveaway

RESULTS_DIR = Path(__file__).parent.parent.absolute() / "outputs"
def read_last_results(result_file:str):
    result_file_path= RESULTS_DIR / result_file
    with open(result_file_path,"r",encoding="utf-8") as r_file:
        for record in r_file:
            print(record)
            
def take_part(tweet_record:dict):
    account_name = tweet_record["account"],
    follow_account(account_name)
    pass
def update_tweet_lists(): 
    list_current_id = []
    with open(RESULTS_DIR / "tweets_historic.json", "r+") as hist_file:
        with open(RESULTS_DIR / "scrap_results.jsonl", "r") as r_file:
            historic = json.load(hist_file)
            for histo_record in historic["tweets"]:
                list_current_id.append(histo_record["id"])
            for new_record in r_file:
                new_record = json.loads(new_record)
                is_giveaway = detect_giveaway(new_record["content"])
                if new_record["id"] not in list_current_id:
                    data = {
                        "id":new_record["id"],
                        "url": new_record["url"],
                        "post_time": new_record["date"],
                        "process_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "is_giveaway": is_giveaway,
                        "status":"not completed"   
                    }
                    historic["tweets"].append(data)
    with open(RESULTS_DIR / "tweets_historic.json","w") as new_hist_file:
        json.dump(historic, new_hist_file)
                
if __name__ == "__main__":
    # read_last_results("scrap_results.jsonl")
    pass