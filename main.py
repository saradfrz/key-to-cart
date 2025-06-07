from config import CSV_FOLDER, DOWNLOAD_FOLDER, LOGIN_URL, NFE_URL_TEMPLATE
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
    )

    try:
        scraper.manual_login()

    finally:
        scraper.driver.quit()


if __name__ == "__main__":
    main()
