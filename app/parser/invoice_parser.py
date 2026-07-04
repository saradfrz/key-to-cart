from bs4 import BeautifulSoup
from app.utils.string import StringUtils
import logging
import re
import os
import csv

class InvoiceParser:
    def __init__(self, filename, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.filename = filename
        self.filepath = os.path.join(self.config.dir.output_html, filename)
        self.id = filename.split("_")[0]
        self.nfce_id = filename.split("_")[1]
        self.str = StringUtils()

        # Read file content
        content = None
        try:
            with open(self.filepath, mode='r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            content = None

        self.soup = BeautifulSoup(content, 'html.parser') if content else None
        self.soup_list = self.soup.find_all('table') if self.soup else None
        self.purchase_data = {}
        self.purchase_items = []
        
    def store_data(self, key, value):
        self.data[key] = value

    def return_data(self):
        return [self.purchase_data, self.purchase_items_data]
    
    def parse_purchase_data(self):
        for soup in self.soup_list:
            try:
                store = self._parse_store(soup)
                if store and not self.purchase_data.get("store"):
                    self.purchase_data["store"] = store

            except Exception as e:
                store = None
                continue

            try:
                [cnpj, store_state_code] = self._parse_store_codes(soup)
                if cnpj and not self.purchase_data.get("cnpj"):
                    self.purchase_data["cnpj"] = cnpj
                    self.purchase_data["store_state_code"] = store_state_code
            except Exception as e:
                cnpj = None
                store_state_code = None
                pass
            try:
                address = self._parse_store_address(soup)
                if address and not self.purchase_data.get("address"):
                    self.purchase_data["address"] = address
            except Exception as e:
                address = None
                pass
            try:
                purchase_date = self._parse_purchase_date(soup)
                if purchase_date and not self.purchase_data.get("purchase_date"):
                    self.purchase_data["purchase_date"] = purchase_date
            except Exception as e:
                purchase_date = None
                pass
            try:
                access_key = self._parse_access_key(soup)
                if access_key and not self.purchase_data.get("access_key"):
                    self.purchase_data["access_key"] = access_key
            except Exception as e:
                access_key = None
                pass


    def parse_purchase_items(self):
        try:
            table = [x for x in self.soup_list if "NFCDetalhe_Item" in str(x)][0]
            items_raw = table.find_all('tr', id=re.compile(r'^Item \+ \d+$'))
            items = []
            for item_raw in items_raw:
                # ["Código", "Descrição", "Qtde", "Un", "Vl Unit", "Vl Total"]
                values = [s.contents[0] for s in item_raw.find_all('td')]
                items.append(values)
            
            self.purchase_items = items # list of lists
            
        except Exception as e:
            self.logger.error(f"Error parsing purchase: {e}")
            purchase = None
            pass

    def _parse_store(self, soup: BeautifulSoup):
        return soup.find('td', {'class': self.config.invoice_parser.store_name__class}).contents[0].strip()

    def _parse_store_codes(self, soup):
        raw_codes = soup.find('td', {'class': self.config.invoice_parser.cnpj_store_state_code__class}).contents[0].strip()
        codes = [s.strip() for s in raw_codes.split('\n')]
        cnpj = codes[1]
        store_state_code = codes[2].replace("Inscrição Estadual: ", "").strip()
        return [cnpj, store_state_code]

    def _parse_store_address(self, soup: BeautifulSoup):
        address = soup.find_all('td', {'class': self.config.invoice_parser.cnpj_store_state_code__class})[1].contents[0].strip()
        return self._replace_multiple_spaces(address)

    def _parse_purchase_date(self, soup: BeautifulSoup):
        soup_list = soup.find_all('td', {'class': self.config.invoice_parser.store_name__class})
        date_raw = [s for s in soup_list if "Data de Emissão" in s.contents[0].strip()][0]
        date_raw = date_raw.contents[0].strip()
        return self._extract_datetime(date_raw)

    def _extract_datetime(self, date_raw):
        pattern = r"\b\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}\b"
        match = re.search(pattern, date_raw)
        return match.group(0) if match else None

    def _parse_access_key(self, soup):
        soup_list = soup.find_all('td', {'class': self.config.invoice_parser.store_name__class})
        raw_access_key = [s for s in soup_list if self._extract_access_key(s.contents[0].strip())]
        return raw_access_key[0].contents[0].replace(" ","") if raw_access_key else None

    def _extract_access_key(self, text):
        pattern = r"(\d{4} ){10}\d{4}"
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    def run(self):
        self.parse_purchase_data() # -> self.purchase_data
        self.parse_purchase_items() # -> self.purchase_items

        purchase = []

        for item in self.purchase_items:
            item_purchase = [self.id]
            item_purchase.extend(self.purchase_data.values())  # Append purchase_data values to each item
            item_purchase.extend(item)  # Append id_purchase and ncfe_id to each item
            purchase.append(item_purchase)

        return purchase
    