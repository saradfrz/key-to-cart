import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import json
from logs.log_handler import setup_logger
from app.data_tools import DataTools

from config import MASTER_DATA

class NFCeScraper:
    def __init__(self, download_folder, login_url, nfce_url_template, nfce_data_dir, cookies_file, user_data_dir, wait_timeout=60):
        self.download_folder = os.path.abspath(download_folder)
        self.login_url = login_url
        self.nfce_url_template = nfce_url_template
        self.wait_timeout = wait_timeout
        self.driver = None
        self.cookies_file = cookies_file
        self.nfce_data_dir = nfce_data_dir
        self.logger = setup_logger(self.__class__.__name__)
        self.user_data_dir = user_data_dir
        self.MASTER_DATA = MASTER_DATA


    def setup_browser(self, headless: bool = False, user_data_dir: str = None):
        options = uc.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        if headless:
            options.add_argument("--headless=new")  # safer headless option for newer Chrome
        if user_data_dir:
            options.add_argument(f"--user-data-dir={str(user_data_dir)}")
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

    def download_nfce_data(self, data):
        for nfce in data:
            key = nfce['Chave de Acesso']
            print(f"Processing nfce with key: {key}")
            try:
                self._access_nfce_html(key)
                self._find_next_button()
                time.sleep(2)
                self._download_html(self._create_unique_key(nfce))
            except Exception as e:
                self.logger.error(f"Access denied for nfce with key {key}. Razão Social: {nfce['Razão Social']}. Data de Emissão: {nfce['Data Emissão']}. Error: {e}")
                continue
            time.sleep(2)       

    def _access_nfce_html(self, key):
        
        driver = self.driver
        with open(self.cookies_file, 'r') as f:
            cookies = json.load(f)
        key = key.replace(" ", "")  # URL encode spaces
        driver.get(f"{self.nfce_url_template}{key}")  # Must load the domain first
        # for cookie in cookies:
        #     if 'sameSite' in cookie:
        #         del cookie['sameSite']  
        #     driver.add_cookie(cookie)
        # # Wait for the page to load
        time.sleep(5)

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
            time.sleep(10)  # Wait for the page to load after clicking
            self.driver = driver
        except Exception as e:
            self.logger.error(f"Failed to find or click 'Avançar' button: {e}")
            raise Exception(f"Failed to find or click 'Avançar' button: {e}")

    def _create_unique_key(self, nfce):
        """
        Builds a normalized nfce filename in the format: YYYYMMDD__AccessKey__StoreName
        """
        access_key = nfce['Chave de Acesso'].replace(" ", "")

        # Format date as YYYYMMDD
        raw_date = nfce['Data Emissão'].strip()
        date_parts = raw_date.split("/")
        formatted_date = "".join(date_parts[::-1])  # DD/MM/YYYY → YYYYMMDD

        # Normalize store name for filesystem safety
        store_name = (
            nfce['Razão Social']
            .strip()
            .replace(" ", "_")
            .replace("/", "")
            .replace("\\", "")
            .lower()
        )
        return f"{formatted_date}__{access_key}__{store_name}"


    def _download_html(self, unique_key):
        driver = self.driver
        nfce_html = driver.page_source
        file_path = os.path.join(self.nfce_data_dir, f"{unique_key}.html")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(nfce_html)

        self.logger.scraping_info(f"Downloaded nfce HTML for key {unique_key} to {file_path}")

    def run(self):
        try:
            self.setup_browser(headless=False, user_data_dir=self.user_data_dir) 
            #scraper.save_cookies_after_manual_login(COOKIES_FILE)
            data_prep = DataTools()
            csv_list = data_prep.get_all_data_files(self.MASTER_DATA, ".csv")
            data = data_prep.get_all_files_content(csv_list, ".csv")
            self.download_nfce_data(data=data)
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please check your setup and try again.")
        finally:
            self.driver.quit()


