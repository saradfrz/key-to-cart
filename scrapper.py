from sefaz_scrapper.config import CSV_FOLDER, DOWNLOAD_FOLDER, LOGIN_URL, NFE_URL_TEMPLATE, USER_DATA_DIR, COOKIES_FILE, NFE_DATA_DIR
from sefaz_scrapper.nfe_scraper import NFEScraper
from sefaz_scrapper.data_prep_for_scrapper import DataPrepForScraper
import json


def main():
    scraper = NFEScraper(
        csv_folder=CSV_FOLDER,
        download_folder=DOWNLOAD_FOLDER,
        login_url=LOGIN_URL,
        nfe_url_template=NFE_URL_TEMPLATE,
        nfe_data_dir=NFE_DATA_DIR,
        cookies_file=COOKIES_FILE,
        wait_timeout=180  
    )

    scraper.setup_browser(
        headless=False, 
        user_data_dir=USER_DATA_DIR  
    )

    try:
        #scraper.save_cookies_after_manual_login(COOKIES_FILE)
        data_prep = DataPrepForScraper(scraper.csv_folder)
        csv_list = data_prep.get_all_data_files()
        data = data_prep.get_all_files_content(csv_list)

        scraper.download_nfe_data(
            data=data
        )


    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your setup and try again.")

    finally:
        scraper.driver.quit()


if __name__ == "__main__":
    main()
