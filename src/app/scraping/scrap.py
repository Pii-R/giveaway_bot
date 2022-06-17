import os, json, datetime
from pathlib import Path
from typing import List

RESULTS_DIR = Path(__file__).parent.parent.absolute() / "outputs"
SOURCE_DIR = Path(__file__).parent.parent.absolute() / "sources"

 
def create_scrap_results_file():
    """create the file outputs/scrap_results.jsonl
    """
    scrap_results = RESULTS_DIR / "scrap_results.jsonl"
    if not scrap_results.is_file():
        with open(RESULTS_DIR / "scrap_results.jsonl", "w", encoding="utf-8") as f:
            pass
 
def export_sources_accounts(file: str):
    """export accounts to scrap from sources.json

    Args:
        file (str): file path where sources.json is located

    Returns:
        _type_: List
    """
    
    with open(file, "r", encoding="utf-8") as sources_file:
        sources = json.load(sources_file)
        list_sources_account = [s["account"] for s in sources["sources"]]
        return list_sources_account


def divide_source_accounts_into_chunks(
    sources_accounts: List, chunk_size: int
) -> List[List]:
    """divide the List of accounts into chunks of size chunk_size

    Args:
        sources_accounts (List): List of accounts to scrap

    Returns:
        List: List of chunks of accounts
    """
    if chunk_size == 0:
        return []
    return [
        sources_accounts[i : i + chunk_size]
        for i in range(0, len(sources_accounts), chunk_size)
    ]


def format_one_sources_chunck_for_query(chunck_source: List) -> str:
    """format the query to scrap with all the accounts from sources.json

    Args:
        sources_account (List): List of accounts to scrap

    Returns:
        str: str formatted for query
    """
    if chunck_source:
        s = f"from:{chunck_source[0]}"
        formated_sources = s
        if len(chunck_source) > 1:
            l = [f" OR from:{s}" for s in chunck_source[1:]]
            formated_sources = "(" + ",".join([s] + l) + ")"
        return formated_sources


def execute_query(sources: List, scraping_params: dict):
    """takes a List of accounts and a dict of params and execute the query t

    Args:
        sources (List): flatten List of accounts to scrap
        scraping_params (dict): dict containing the params to scrap
    """
    output_scrap_file = RESULTS_DIR / "scrap_results.jsonl"
    create_scrap_results_file()
    search = scraping_params["search"]
    search_class = scraping_params["class_search"]
    max_results = scraping_params["max_results"]
    start_time = scraping_params["start_time"]
    sources = export_sources_accounts(SOURCE_DIR / "sources.json") 
    chunck_sources = divide_source_accounts_into_chunks(sources, 5)
    with open(RESULTS_DIR / "global_scrap_results.jsonl", "a", encoding="utf-8") as g:
        for i, chunck_source in enumerate(chunck_sources):
            formatted_chunck_source = format_one_sources_chunck_for_query(chunck_source)
            command = f"""snscrape --jsonl --max-results {max_results} {search_class} "{formatted_chunck_source} {search} since:{start_time} exclude:replies" > {output_scrap_file}"""
            os.system(command)
            with open(output_scrap_file, "r", encoding="utf-8") as f:
                g.write(f.read())


def run_scraping(scraping_params: dict):
    """run the scraping of all the accounts from sources.json
    Then it will save the results in outputs/scrap_results.json

    Args:
        params (dict): {max_result:int,search:int,class:str}
    """
    sources = export_sources_accounts(SOURCE_DIR / "sources.json")
    execute_query(sources, scraping_params)


if __name__ == "__main__":
    scraping_params = {
        "search": "#concours",
        "class_search": "twitter-search",
        "max_results": 10,
        "start_time": "",
    }
    # run_scraping(scraping_params)
    sources = ["TopAchat", "TopAchat"]
    execute_query(sources, scraping_params)
