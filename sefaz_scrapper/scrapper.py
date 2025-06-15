from config import CSV_FOLDER, DOWNLOAD_FOLDER, SEFAZ_LOGIN_URL, NFCE_URL_TEMPLATE_URL_TEMPLATE, USER_DATA_DIR, COOKIES_FILE, nfce_data_DIR
from sefaz_scrapper.nfce_scraper import NFCE_URL_TEMPLATEScraper
from data_tools import DataTools


def run_scrapper():
    scraper = NFCE_URL_TEMPLATEScraper(
        csv_folder=CSV_FOLDER,
        download_folder=DOWNLOAD_FOLDER,
        login_url=SEFAZ_LOGIN_URL,
        NFCE_URL_TEMPLATE_url_template=NFCE_URL_TEMPLATE_URL_TEMPLATE,
        nfce_data_dir=nfce_data_DIR,
        cookies_file=COOKIES_FILE,
        wait_timeout=180  
    )

    scraper.setup_browser(
        headless=False,
        user_data_dir=USER_DATA_DIR  
    )

    try:
        #scraper.save_cookies_after_manual_login(COOKIES_FILE)
        data_prep = DataTools(scraper.csv_folder)
        csv_list = data_prep.get_all_data_files(".csv")
        data = data_prep.get_all_files_content(csv_list, ".csv")

        scraper.download_nfce_data(
            data=data
        )


    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your setup and try again.")

    finally:
        scraper.driver.quit()

