
import logging
import os
import shutil

from app.utils.directory import DirectoryManager
from app.utils.file import FileManager
from app.source.invoice_source import InvoiceSource
from app.downloader.invoice_downloader import InvoiceDownloader 
from app.parser.invoice_parser import InvoiceParser

class InvoicePipeline:

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.dir = DirectoryManager()
        self.file = FileManager()
        self.source = InvoiceSource(config)
        self.downloader = InvoiceDownloader(config)

    def run(self):

        # Get the list of invoice NFCe codes from the source
        invoice_nfce_codes = self.source.run()
        invoice_nfce_codes = list(set(invoice_nfce_codes))  # Remove duplicates

        # Scrap invoices from the source and download them
        for x, nfce_code in enumerate(invoice_nfce_codes):
            nfce_id = x + 1
            try:                
                print(f"Processing nfce {nfce_id}/{len(invoice_nfce_codes)} with key: {nfce_code}")
                self.downloader.run(nfce_code, nfce_id)       
            except Exception as e:
                self.logger.error(f"An error occurred while scrapping {nfce_code}: {e}")
                continue

        # Parse the downloaded invoices
        purchases = []
        html_files = sorted(self.dir.list_files(self.config.dir.output_html, extension=".html"))
        for x, html_file in enumerate(html_files):
            nfce_id = x + 1
            try:
                print(f"Parsing nfce {nfce_id}/{len(html_files)}: {html_file}")
                parser = InvoiceParser(html_file, self.config)
                purchase = parser.run()
                if purchase:
                    purchases.extend(purchase)
            except Exception as e:
                self.logger.error(f"An error occurred while parsing {html_file}: {e}")
                continue
        
        # Export the parsed data to CSV
        purchase_columns = [
            "id_scrapping",
            "nm_store",
            "id_cnpj",
            "id_store_state_code",
            "dt_purchase",
            "id_nfce",
            "id_item",
            "ds_item",
            "qt_item",
            "tp_unit",
            "vl_unit",
            "vl_total"
            ]
        
        self.file.save_csv(f"{self.config.dir.output}/{self.config.year}_purchase_data_items.csv", purchase_columns, purchases)

