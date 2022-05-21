import os 
from pathlib import Path
from datetime import datetime


RESULTS_DIR = Path(__file__).parent.parent.absolute() / "outputs"
def run_scraping(params:dict):
    """_summary_

    Args:
        params (dict): {max_result:int,search:int,class:str}
    """    
    filename = RESULTS_DIR / "scrap_results.json"
    command = f"snscrape --jsonl --max-results 10 twitter-search 'from:TopAchat #concours exclude:replies' > {filename}"
    os.system(command)

if __name__ == "__main__":
    run_scraping({})
