import os, json, datetime
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent.absolute() / "outputs"
SOURCE_DIR = Path(__file__).parent.parent.absolute() / "sources"


def export_sources_accounts(file: str):
    """export accounts to scrap from sources.json

    Args:
        file (str): file path where sources.json is located

    Returns:
        _type_: list
    """
    with open(file, "r", encoding="utf-8") as sources_file:
        sources = json.load(sources_file)
        list_sources_account = [s["account"] for s in sources["sources"]]
        return list_sources_account


def format_sources_for_query(sources_account: list):
    """format the query to scrap with all the accounts from sources.json

    Args:
        sources_account (list): list of accounts to scrap

    Returns:
        str: str formatted for query
    """
    if sources_account:
        s = f"from:{sources_account[0]}"
        formated_sources = s
        if len(sources_account) > 1:
            l = [f" OR from:{s}" for s in sources_account[1:]]
            formated_sources = "(" + ",".join([s] + l) + ")"
        return formated_sources


def run_scraping(scraping_params: dict):
    """run the scraping of all the accounts from sources.json
    Then it will save the results in outputs/scrap_results.json

    Args:
        params (dict): {max_result:int,search:int,class:str}
    """
    # date = datetime.datetime.now().strftime("%Y-%m-%d")
    date = "2022-05-10"
    search = scraping_params["search"]
    search_class = scraping_params["class_search"]
    max_results = scraping_params["max_results"]
    filename = RESULTS_DIR / "scrap_results.jsonl"
    sources = export_sources_accounts(SOURCE_DIR / "sources.json")
    formated_sources = format_sources_for_query(sources)
    command = f"snscrape --jsonl --max-results {max_results} {search_class} '{formated_sources} {search} since:{date} exclude:replies' > {filename}"
    print(f"run scraping...\n{max_results} tweets are scraped")
    os.system(command)


if __name__ == "__main__":
    scraping_params = {
        "search": "#concours",
        "class_search": "twitter-search",
        "max_results": 30,
        "start_time": "",
    }
    run_scraping(scraping_params)
