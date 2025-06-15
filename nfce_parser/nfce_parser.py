from bs4 import BeautifulSoup
from logs.log_handler import setup_logger
import re
from config import (
    STORE_NAME__CLASS, 
    CNPJ_STORE_STATE_CODE__CLASS
    )


class NFCeParser:
    def __init__(self, file_content):
        """
        Initialize the NFCeParser with the content of a file.
        Args:
        file_content (str): The content of the file to parse.
        """
        soup = BeautifulSoup(file_content, 'html.parser') if file_content else None
        self.soup = soup.find('table')
        self.data = {}
        self.logger = setup_logger(self.__class__.__name__)

        
    def store_data(self, key, value):
        """
        Store data in the parser's data dictionary.
        Args:
        key (str): The key under which to store the value.
        value (any): The value to store.
        """
        self.data[key] = value

    def return_data(self):
        """
        Return the data stored in the parser.
        Returns:
        dict: The data dictionary.
        """
        return self.data
    
    def parse(self):
        """
        Parse the file content and extract relevant data.
        This method should be implemented in subclasses.
        """
        try:
            self.store_data("store", self._parse_store())
        except Exception as e:
            self.logger.error(f"Error parsing store: {e}")
            pass
        try:
            [cnpj, store_state_code] = self._parse_store_codes()
            self.store_data("cnpj", cnpj)
            self.store_data("store_state_code", store_state_code)
        except Exception as e:
            self.logger.error(f"Error parsing cnpj/store_state_code: {e}")
            pass
        try:
            self.store_data("store_address", self._parse_store_address())
        except Exception as e:
            self.logger.error(f"Error parsing store_address: {e}")
            pass
        try:
            self.store_data("purchase_date", self._parse_purchase_date())
        except Exception as e:
            self.logger.error(f"Error parsing purchase_date: {e}")
            pass
        try:
            self.store_data("access_key", self._parse_access_key())
        except Exception as e:
            self.logger.error(f"Error parsing access_key: {e}")
            pass
        try:
            self.store_data("purchase", self._parse_purchase())
        except Exception as e:
            self.logger.error(f"Error parsing purchase: {e}")
            pass

    def _parse_store(self):
        return self.soup.find('td', {'class': STORE_NAME__CLASS}).contents[0].strip()

    def _parse_store_codes(self):
        raw_codes = self.soup.find('td', {'class': CNPJ_STORE_STATE_CODE__CLASS}).contents[0].strip()
        codes = [s.strip() for s in raw_codes.split('\n')]
        cnpj = codes[1]
        store_state_code = codes[2].replace("Inscrição Estadual: ", "").strip()
        return [cnpj, store_state_code]

    def _parse_store_address(self):
        pass

    def _parse_purchase_date(self):
        pass

    def _parse_access_key(self):
        pass

    def _parse_purchase(self):
        pass