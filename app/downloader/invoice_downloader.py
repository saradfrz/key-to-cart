import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
        self.failed_nfce = None

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
        

    def find_next_button(self):
        driver = self.driver
        try:
            driver.switch_to.default_content()
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            if len(iframes) == 0:
                return None

            frame_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
            )
            driver.switch_to.frame(frame_element)

            time.sleep(5) # Wait for the iframe content to load
            next_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Avançar']"))
            )
            next_button.click()
            
            time.sleep(3)  # Wait for the page to load after clicking
            self.driver = driver
        except Exception as e:
            self.logger.error(f"Failed to find or click 'Avançar' button: {e}")
            raise Exception(f"Failed to find or click 'Avançar' button: {e}")


    def access_nfce_html(self, key):
        driver = self.driver
        driver.get(f"{self.nfce_url_template}{key}")  # Must load the domain first
        time.sleep(7)

        if "Acesso Negado" in driver.page_source:
            self.logger.error(f"Acesso Negado")

        self.find_next_button()


    def create_unique_key(self, nfce, id):
        access_key = nfce.replace(" ", "")
        return f"{id}_{access_key}"

    def get_html(self, unique_key):
        driver = self.driver
        time.sleep(3)  # Ensure the page is fully loaded

        # Dismiss any alert before interacting with the page
        alert_text = self._dismiss_alert_if_present()
        if alert_text:
            self.logger.info(f"Skipping key {unique_key} due to alert: {alert_text}")
            return None  # signal to caller that this key failed

        return driver.page_source
    
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
        
        for x in range(5):  # Retry up to 5 times
            success = False
            try:
                if x < 2:
                    time.sleep(5)
                    self.access_nfce_html(nfce)
                if x >= 2:
                    time.sleep(x*3)
                    self.find_next_button()
                    time.sleep(x*3)
                nfce_html = self.get_html(f"{nfce_id}_{nfce}")

                if not nfce_html:
                    print(f"Skipping key {nfce_id}_{nfce} due to alert or failed page load.")
                    self.failed_nfce = [nfce_id, nfce]
                    return False

                if "case '12': return {'uf':'AC', 'ext':'do Acre' };" in  nfce_html:
                    success = True
                    file_path = os.path.join(self.config.dir.output_html, f"{nfce_id}_{nfce}.html")
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(nfce_html)
                    print(f"Downloaded nfce HTML for key {nfce_id}_{nfce} to {file_path}")            
                    time.sleep(2)   
                    return True  # Successfully downloaded and saved the HTML

                if x == 4 and not success:
                    self.logger.error(f"Failed to download valid HTML for {nfce} after 5 attempts.")
                    return False  # Failed after 5 attempts
            except Exception as e:
                self.logger.error(f"Error downloading HTML for {nfce} on attempt {x+1}: {e}")                    
            time.sleep(5)
        
            

