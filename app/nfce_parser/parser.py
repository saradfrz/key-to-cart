from bs4 import BeautifulSoup
from logs.log_handler import setup_logger
import re
from config import (
    STORE_NAME__CLASS, 
    CNPJ_STORE_STATE_CODE__CLASS
    )
from app.data_tools import DataTools
import os
import csv

class NFCeParser:
    def __init__(self, file_path, NFCE_DATA_DIR, PARSER_OUTPUT_FOLDER):
        """
        Initialize the NFCeParser with a path to an HTML file.
        Args:
            file_path (str): Path to the HTML file to parse.
        """
        self.NFCE_DATA_DIR = NFCE_DATA_DIR
        self.PARSER_OUTPUT_FOLDER = PARSER_OUTPUT_FOLDER
        self.file_path = file_path

        # Read file content
        content = None
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            content = None

        soup = BeautifulSoup(content, 'html.parser') if content else None
        self.soup = soup.find('table') if soup else None
        self.purchase_data = []
        self.purchase_items_data = []
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
        return [self.purchase_data, self.purchase_items_data]
    
    def parse(self):
        """
        Parse the file content and extract relevant data.
        This method should be implemented in subclasses.
        """
        try:
            store = self._parse_store()
        except Exception as e:
            self.logger.error(f"Error parsing store: {e}")
            store = None
            pass
        try:
            [cnpj, store_state_code] = self._parse_store_codes()
        except Exception as e:
            self.logger.error(f"Error parsing cnpj/store_state_code: {e}")
            cnpj = None
            store_state_code = None
            pass
        try:
            address = self._parse_store_address()
        except Exception as e:
            self.logger.error(f"Error parsing store_address: {e}")
            address = None
            pass
        try:
            purchase_date = self._parse_purchase_date()
        except Exception as e:
            self.logger.error(f"Error parsing purchase_date: {e}")
            purchase_date = None
            pass
        try:
            access_key = self._parse_access_key()
        except Exception as e:
            self.logger.error(f"Error parsing access_key: {e}")
            access_key = None
            pass

        self.purchase_data = [store, cnpj, store_state_code, address, purchase_date, access_key]

        try:
            purchase = self._parse_purchase()
        except Exception as e:
            self.logger.error(f"Error parsing purchase: {e}")
            purchase = None
            pass
        for item in purchase if purchase else []:
            item.extend([access_key])
            self.purchase_items_data.append(item)


    def _parse_store(self):
        """
        Parses the store name from the HTML and returns it.
        """
        return self.soup.find('td', {'class': STORE_NAME__CLASS}).contents[0].strip()

    def _parse_store_codes(self):
        """
        Parses the CNPJ and store state code from the HTML and returns them as a list [CNPJ, store_state_code].
        """
        raw_codes = self.soup.find('td', {'class': CNPJ_STORE_STATE_CODE__CLASS}).contents[0].strip()
        codes = [s.strip() for s in raw_codes.split('\n')]
        cnpj = codes[1]
        store_state_code = codes[2].replace("Inscrição Estadual: ", "").strip()
        return [cnpj, store_state_code]

    def _parse_store_address(self):
        """
        Parses the store address from the HTML and returns it.
        """
        address = self.soup.find_all('td', {'class': CNPJ_STORE_STATE_CODE__CLASS})[1].contents[0].strip()
        return self._replace_multiple_spaces(address)
    

    def _parse_purchase_date(self):
        """
        Parses the purchase date from the HTML and returns it.
        """
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
        """
        Parses the access key from the HTML and returns it.
        """
        soup_list = self.soup.find_all('td', {'class': STORE_NAME__CLASS})
        raw_access_key = [s for s in soup_list if self._extract_access_key(s.contents[0].strip())]
        return raw_access_key[0].contents[0].replace(" ","") if raw_access_key else None


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

    def _parse_purchase(self) -> list[list[str]]:
        """
        Parses the purchase items from the HTML and returns them as a list of items bought in the purchase.
        """
        table = self.soup.find_all('table')[1]
        items_raw = table.find_all('tr', id=re.compile(r'^Item \+ \d+$'))
        items = []
        for item_raw in items_raw:
            # ["Código", "Descrição", "Qtde", "Un", "Vl Unit", "Vl Total"]
            values = [s.contents[0] for s in item_raw.find_all('td')]
            items.append(values)
        return items
    
    def run(self):
        """
        Parse the file provided to this parser instance and write the JSON output.
        """
        data_tools = DataTools()

        # Parse the current file (self.file_path)
        self.parse()
        [purchase_data, purchase_items_data] = self.return_data()

        unique_key = data_tools.create_unique_key(
            purchase_data[5],
            purchase_data[4].split(" ")[0] if purchase_data[4].split(" ")[0] else "",
            purchase_data[0]
        )

        purchase_data_items_filename = os.path.join(self.PARSER_OUTPUT_FOLDER, f"{unique_key}_purchase_items_data.csv")      
        purchase_data_items_columns = ["Código", "Descrição", "Qtde", "Un", "Vl Unit", "Vl Total"]

        with open(purchase_data_items_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(purchase_data_items_columns)
            csv_writer.writerows(purchase_items_data)           

        return purchase_data
        





