import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

class NFEScraper:
    def __init__(self, csv_folder, download_folder, login_url, nfe_url_template, wait_timeout=60):
        self.csv_folder = csv_folder
        self.download_folder = os.path.abspath(download_folder)
        self.login_url = login_url
        self.nfe_url_template = nfe_url_template
        self.wait_timeout = wait_timeout
        self.driver = None

    def setup_browser(self, headless=False, user_data_dir=None):
        options = Options()

        # Download folder preferences
        prefs = {
            "download.default_directory": self.download_folder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        options.add_experimental_option("prefs", prefs)

        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

        if user_data_dir:
            options.add_argument(f'--user-data-dir={user_data_dir}')
            options.add_argument("--profile-directory=Default")

        options.add_argument("--disable-blink-features=AutomationControlled")

        # IMPORTANT: With Selenium 3.x, you **must** pass the executable path manually
        # undetected-chromedriver will provide this path via uc.install()

        driver_path = uc.install()  # downloads driver if needed, returns path

        self.driver = uc.Chrome(executable_path=driver_path, options=options)
        self.driver.set_page_load_timeout(60)

        print(f"[INFO] Undetected Chrome started with download folder: {self.download_folder}")

    def manual_login(self):
        if not self.driver:
            raise RuntimeError("Browser not initialized. Call setup_browser() first.")
        self.driver.get(self.login_url)
        print(f"[INFO] Please log in manually within {self.wait_timeout} seconds...")
        time.sleep(self.wait_timeout)
