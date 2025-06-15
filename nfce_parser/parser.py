from nfce_parser.nfce_parser import NFCeParser
from data_tools import DataTools
from config import NFCE_DATA_DIR, PARSER_OUTPUT_FOLDER
import os
import json

def run_parser():
    data_tools = DataTools(NFCE_DATA_DIR, ".html")
    files = data_tools.get_all_files_content(
        data_tools.get_all_data_files()
    )
    for file in files:
        scraper = NFCeParser(file)
        scraper.parse()
        data = scraper.return_data()
        unique_key = data_tools.create_unique_key(
            data.get("access_key", ""),
            data.get("purchase_date", "").split(" ")[0], 
            data.get("store", "")
        )
        filename = os.path.join(PARSER_OUTPUT_FOLDER, f"{unique_key}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

