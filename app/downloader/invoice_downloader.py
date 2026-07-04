import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import logging


class InvoiceDownloader:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.download_folder = os.path.abspath(self.config.invoice_downloader.download_folder)
        self.login_url = self.config.invoice_downloader.sefaz_login_url
        self.nfce_url_template = self.config.invoice_downloader.nfce_url_template
        self.wait_timeout = self.config.invoice_downloader.wait_timeout
        self.driver = None

        self.setup_browser(headless=False, user_data_dir=self.config.invoice_downloader.user_data_dir)

    def setup_browser(self, headless: bool = False, user_data_dir: str = None):
        options = uc.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        if headless:
            options.add_argument("--headless=new")  # safer headless option for newer Chrome
        if user_data_dir:
            options.add_argument(f"--user-data-dir={str(user_data_dir)}")
        self.driver = uc.Chrome(version_main=149)
        self.driver.set_page_load_timeout(180)
        self.logger.info(f"Undetected Chrome started with download folder: {self.download_folder}")

    def access_nfce_html(self, key):
        driver = self.driver
        key = key.replace(" ", "")  # URL encode spaces
        driver.get(f"{self.nfce_url_template}{key}")  # Must load the domain first
        time.sleep(5)

        if "Acesso Negado" in driver.page_source:
            self.logger.error(f"Acesso Negado")

    def find_next_button(self):
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

    def create_unique_key(self, nfce, id):
        access_key = nfce.replace(" ", "")
        return f"{id}_{access_key}"

    def download_html(self, unique_key):
        driver = self.driver
        time.sleep(5)  # Ensure the page is fully loaded

        # Dismiss any alert before interacting with the page
        alert_text = self._dismiss_alert_if_present()
        if alert_text:
            self.logger.info(f"Skipping key {unique_key} due to alert: {alert_text}")
            return False  # signal to caller that this key failed

        nfce_html = driver.page_source
        file_path = os.path.join(self.config.dir.output_html, f"{unique_key}.html")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(nfce_html)

        self.logger.info(f"Downloaded nfce HTML for key {unique_key} to {file_path}")
        return True
    
    def _dismiss_alert_if_present(self):
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            self.logger.info(f"Dismissed alert: {alert_text}")
            alert.accept()  # clicks OK
            return alert_text
        except Exception as e:
            return None
        
    def  quit(self):
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed.")

    def run(self, nfce, nfce_id):
        self.access_nfce_html(nfce)
        self.find_next_button()
        time.sleep(3)
        self.download_html(self.create_unique_key(nfce, nfce_id))
        time.sleep(2)   


