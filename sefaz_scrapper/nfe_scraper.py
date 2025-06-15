import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import json
from logs.log_handler import setup_logger

class NFEScraper:
    def __init__(self, csv_folder, download_folder, login_url, nfe_url_template, nfe_data_dir, cookies_file, wait_timeout=60):
        self.csv_folder = csv_folder
        self.download_folder = os.path.abspath(download_folder)
        self.login_url = login_url
        self.nfe_url_template = nfe_url_template
        self.wait_timeout = wait_timeout
        self.driver = None
        self.cookies_file = cookies_file
        self.nfe_data_dir = nfe_data_dir
        self.logger = setup_logger(self.__class__.__name__)

    def setup_browser(self, headless: bool = False, user_data_dir: str = None):
        options = uc.ChromeOptions()

        options.add_argument('--disable-blink-features=AutomationControlled')

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

    def download_nfe_data(self, data):

        for nfe in data:
            key = nfe['Chave de Acesso']
            print(f"Processing NFE with key: {key}")
            try:
                self._access_nfe_html(key)
                self._find_next_button()
                self._download_html(self._create_unique_key(nfe))
            except Exception as e:
                self.logger.error(f"Access denied for NFE with key {key}. Razão Social: {nfe['Razão Social']}. Data de Emissão: {nfe['Data Emissão']}. Error: {e}")
                continue
            time.sleep(2)       

    def _access_nfe_html(self, key):
        
        driver = self.driver
        with open(self.cookies_file, 'r') as f:
            cookies = json.load(f)
        key = key.replace(" ", "")  # URL encode spaces
        driver.get(f"{self.nfe_url_template}{key}")  # Must load the domain first
        # for cookie in cookies:
        #     if 'sameSite' in cookie:
        #         del cookie['sameSite']  
        #     driver.add_cookie(cookie)
        # # Wait for the page to load
        time.sleep(10)

        if "Acesso Negado" in driver.page_source:
            self.logger.error(f"Acesso Negado")

    def _find_next_button(self):
        driver = self.driver
        try:
            # Switch to the iframe containing the button
            iframe = driver.find_element('tag name', 'iframe')
            driver.switch_to.frame(iframe)
            # Find and click the button with value 'Avançar'
            next_button = driver.find_element('xpath', "//input[@type='submit' and @value='Avançar']")
            next_button.click()


            # here i see the data, i can inspect the data in the driver html but i cant extract it
            time.sleep(5)  # Wait for the page to load after clicking
            self.driver = driver
        except Exception as e:
            self.logger.error(f"Failed to find or click 'Avançar' button: {e}")
            raise Exception(f"Failed to find or click 'Avançar' button: {e}")

    def _create_unique_key(self, nfe):
        """
        Builds a normalized NFE filename in the format: YYYYMMDD__AccessKey__StoreName
        """
        access_key = nfe['Chave de Acesso'].replace(" ", "")

        # Format date as YYYYMMDD
        raw_date = nfe['Data Emissão'].strip()
        date_parts = raw_date.split("/")
        formatted_date = "".join(date_parts[::-1])  # DD/MM/YYYY → YYYYMMDD

        # Normalize store name for filesystem safety
        store_name = (
            nfe['Razão Social']
            .strip()
            .replace(" ", "_")
            .replace("/", "")
            .replace("\\", "")
            .lower()
        )
        return f"{formatted_date}__{access_key}__{store_name}"


    def _download_html(self, unique_key):
        driver = self.driver
        nfe_html = driver.page_source
        file_path = os.path.join(self.nfe_data_dir, f"{unique_key}.html")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(nfe_html)

        self.logger.scraping_info(f"Downloaded NFE HTML for key {unique_key} to {file_path}")


