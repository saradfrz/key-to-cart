from config import CSV_FOLDER, DOWNLOAD_FOLDER, LOGIN_URL, NFE_URL_TEMPLATE, USER_DATA_DIR, COOKIES_PATH
from nfe_scraper import NFEScraper


def main():
    scraper = NFEScraper(
        csv_folder=CSV_FOLDER,
        download_folder=DOWNLOAD_FOLDER,
        login_url=LOGIN_URL,
        nfe_url_template=NFE_URL_TEMPLATE,
        wait_timeout=180  # You can parameterize this if needed
    )

    scraper.setup_browser(
        headless=False,  # Change to True if needed
        user_data_dir=USER_DATA_DIR  # Path to your Chrome user data directory
    )

    try:
        #scraper.save_cookies_after_manual_login(COOKIES_PATH)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your setup and try again.")

    finally:
        scraper.driver.quit()


if __name__ == "__main__":
    main()
