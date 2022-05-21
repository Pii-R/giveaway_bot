#coding: utf-8
from pathlib import Path
import json

RESULTS_DIR = Path(__file__).parent.absolute() / "outputs"
def read_last_results(result_file:str):
    result_file_path= RESULTS_DIR / result_file
    with open(result_file_path,"r",encoding="utf-8") as r_file:
        result = json.load(r_file)
        print(result)
        
if __name__ == "__main__":
    read_last_results("scrap_results.json")