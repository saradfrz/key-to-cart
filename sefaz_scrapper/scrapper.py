from config import CSV_FOLDER, DOWNLOAD_FOLDER, SEFAZ_LOGIN_URL, NFCE_URL_TEMPLATE, USER_DATA_DIR, COOKIES_FILE, NFCE_DATA_DIR
from sefaz_scrapper.nfce_scraper import NFCeScraper
from data_tools import DataTools


def run_scrapper():
    scraper = NFCeScraper(
        csv_folder=CSV_FOLDER,
        download_folder=DOWNLOAD_FOLDER,
        login_url=SEFAZ_LOGIN_URL,
        nfce_url_template=NFCE_URL_TEMPLATE,
        nfce_data_dir=NFCE_DATA_DIR,
        cookies_file=COOKIES_FILE,
        wait_timeout=180  
    )
    try:
        scraper.setup_browser(headless=False, user_data_dir=USER_DATA_DIR) 
        #scraper.save_cookies_after_manual_login(COOKIES_FILE)
        data_prep = DataTools(scraper.csv_folder, ".csv")
        csv_list = data_prep.get_all_data_files()
        data = data_prep.get_all_files_content(csv_list)
        scraper.download_nfce_data(data=data)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your setup and try again.")
    finally:
        scraper.driver.quit()

