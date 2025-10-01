from app.sefaz_scrapper.scrapper import NFCeScraper
from app.nfce_parser.parser import NFCeParser
from app.data_tools import DataTools
import os
from config import DOWNLOAD_FOLDER, SEFAZ_LOGIN_URL, NFCE_URL_TEMPLATE, USER_DATA_DIR, COOKIES_FILE, NFCE_DATA_DIR, PARSER_OUTPUT_FOLDER
import csv
import pandas as pd

if __name__ == "__main__":
    nfce_scrapper = NFCeScraper(
        DOWNLOAD_FOLDER,
        SEFAZ_LOGIN_URL,
        NFCE_URL_TEMPLATE,
        NFCE_DATA_DIR,
        COOKIES_FILE,
        USER_DATA_DIR,
        wait_timeout=180
    )

    nfce_scrapper.run()

    breakpoint()

    tools = DataTools()
    pages = tools.get_all_data_files(
        NFCE_DATA_DIR,
        '.html'
    )

    purchase_data_columns = ["store", "cnpj", "store_state_code", "store_address", "purchase_date", "access_key"]
    with open("output/nfce/csv/purchase_data.csv", 'a+', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(purchase_data_columns)

    purchase_data = []
    for page in pages:
        try:
            nfce_parser = NFCeParser(
                page,
                NFCE_DATA_DIR,
                PARSER_OUTPUT_FOLDER
            )
            
            single_purchase_data = nfce_parser.run()
            if single_purchase_data != []:
                purchase_data.extend(single_purchase_data)
                with open(f"{PARSER_OUTPUT_FOLDER}/purchase_data.csv", 'a+', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(single_purchase_data)
        except Exception as e:
            print(f"An error has ocurred: {str(e).replace("\n"," ")}")
            continue

    

          
