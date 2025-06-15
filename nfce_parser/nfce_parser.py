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
        address = self.soup.find_all('td', {'class': CNPJ_STORE_STATE_CODE__CLASS})[1].contents[0].strip()
        return self._replace_multiple_spaces(address)
    

    def _parse_purchase_date(self):
        soup_list = self.soup.find_all('td', {'class': STORE_NAME__CLASS})
        date_raw = [s for s in soup_list if "Data de Emissão" in s.contents[0].strip()][0]
        date_raw = date_raw.contents[0].strip()
        return self._extract_datetime(date_raw)

    def _extract_datetime(self, date_raw):
        """
        Extracts and returns a datetime string in the pattern dd/dd/dddd dd:dd:dd from the input string.
        Args:
            date_raw (str): The raw string containing the date and time.
        Returns:
            str or None: The matched datetime string, or None if not found.
        """
        pattern = r"\b\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}\b"
        match = re.search(pattern, date_raw)
        return match.group(0) if match else None

    def _parse_access_key(self):
        soup_list = self.soup.find_all('td', {'class': STORE_NAME__CLASS})
        raw_access_key = [s for s in soup_list if self._extract_access_key(s.contents[0].strip())]
        return raw_access_key[0].contents[0] if raw_access_key else None


    def _extract_access_key(self, text):
        """
        Extracts and returns a string matching the NFE access key pattern:
        11 groups of 4 digits separated by spaces (e.g., 4321 0189 8972 ...).
        Args:
            text (str): The input string to search.
        Returns:
            str or None: The matched access key string, or None if not found.
        """
        pattern = r"(\d{4} ){10}\d{4}"
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    def _replace_multiple_spaces(self, text):
        """
        Replaces multiple spaces in a string with a single space.
        Args:
            text (str): The input string.
        Returns:
            str: The modified string with multiple spaces replaced by a single space.
        """
        return re.sub(r'\s+', ' ', text).strip()

    def _parse_purchase(self):
        pass