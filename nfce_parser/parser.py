from nfce_parser.nfce_parser import NFCeParser
from data_tools import DataTools
from config import NFCE_DATA_DIR

def run_parser():
    data_tools = DataTools(NFCE_DATA_DIR, ".html")
    files = data_tools.get_all_files_content(
        data_tools.get_all_data_files()
    )
    for file in files:
        scraper = NFCeParser(file)
        scraper.parse()
        data = scraper.return_data()
