import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import json

class NFEScraper:
    def __init__(self, csv_folder, download_folder, login_url, nfe_url_template, wait_timeout=60):
        self.csv_folder = csv_folder
        self.download_folder = os.path.abspath(download_folder)
        self.login_url = login_url
        self.nfe_url_template = nfe_url_template
        self.wait_timeout = wait_timeout
        self.driver = None
        self.cookies_file = os.path.join(self.download_folder, 'cookies.json')

    def setup_browser(self, headless: bool = False, user_data_dir: str = None):
        options = uc.ChromeOptions()

        # 1. Headless mode
        if headless:
            options.add_argument("--headless=new")  # safer headless option for newer Chrome

        # 2. User data dir
        if user_data_dir:
            options.add_argument(f"--user-data-dir={str(user_data_dir)}")


        # 5. Start Chrome
        self.driver = uc.Chrome()
        self.driver.set_page_load_timeout(180)

        print(f"[INFO] Undetected Chrome started with download folder: {self.download_folder}")


    def save_cookies_after_manual_login(self, cookies_file):
        driver = self.driver
        driver.get(self.login_url)

        print("Login manually, then press Enter here.")
        input()

        cookies = driver.get_cookies()
        with open(cookies_file, 'w') as f:
            json.dump(cookies, f, indent=4)

        print(f"Cookies saved to {cookies_file}")
        driver.quit()

    def load_cookies_to_driver(self, domain):
        driver = self.driver
        with open(self.cookies_file, 'r') as f:
            cookies = json.load(f)

        driver.get(domain)  # Must load the domain first
        for cookie in cookies:
            if 'sameSite' in cookie:
                del cookie['sameSite']  
            driver.add_cookie(cookie)