import os 
from pathlib import Path
import json

RESULTS_DIR = Path(__file__).parent.parent.absolute() / "outputs"
SOURCE_DIR = Path(__file__).parent.parent.absolute() / "sources"

def export_sources_accounts(file:str):
    with open(file, "r",encoding = 'utf-8') as sources_file:
        sources = json.load(sources_file)
        list_sources_account = [s["account"] for s in sources["sources"]]
        return list_sources_account
    
def format_sources_for_query(sources_account:set):
    if sources_account:
        s = f"from:{sources_account[0]}"
        formated_sources  = s
        if len(sources_account)>1:
            l = [f" OR from:{s}" for s in sources_account[1:]]
            formated_sources = "("+",".join([s]+l)+")"
        return formated_sources
    
def run_scraping(params:dict):
    """_summary_

    Args:
        params (dict): {max_result:int,search:int,class:str}
    """    
    filename = RESULTS_DIR / "scrap_results.jsonl"
    sources = export_sources_accounts(SOURCE_DIR / "sources.json")
    formated_sources = format_sources_for_query(sources)
    command = f"snscrape --jsonl --max-results 50 twitter-search '{formated_sources} #concours exclude:replies' > {filename}"
    os.system(command)

if __name__ == "__main__":
    run_scraping({})
