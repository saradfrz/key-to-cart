from config import CSV_FOLDER, DOWNLOAD_FOLDER, LOGIN_URL, NFE_URL_TEMPLATE, USER_DATA_DIR, COOKIES_PATH
from nfe_scraper import NFEScraper
from data_prep_for_scrapper import DataPrepForScraper
import json


def main():
    scraper = NFEScraper(
        csv_folder=CSV_FOLDER,
        download_folder=DOWNLOAD_FOLDER,
        login_url=LOGIN_URL,
        nfe_url_template=NFE_URL_TEMPLATE,
        wait_timeout=180  
    )

    scraper.setup_browser(
        headless=False, 
        user_data_dir=USER_DATA_DIR  
    )

    try:
        #scraper.save_cookies_after_manual_login(COOKIES_PATH)
        data_prep = DataPrepForScraper(scraper.csv_folder)
        csv_list = data_prep.get_all_data_files()
        data = data_prep.get_all_files_content(csv_list)
        # Save data to JSON file
        with open('all_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    

        scraper.extract_nfe_data(
            data=data,
            cookies_file=COOKIES_PATH,
            user_data_dir=USER_DATA_DIR
        )


    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your setup and try again.")

    finally:
        scraper.driver.quit()


if __name__ == "__main__":
    main()
