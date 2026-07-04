
import logging
import os
import shutil

from app.utils.directory import DirectoryManager
from app.source.invoice_source import InvoiceSource
from app.downloader.invoice_downloader import InvoiceDownloader 
from app.parser.invoice_parser import InvoiceParser
# from app.exporter.invoice_exporter import InvoiceExporter

class InvoicePipeline:

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.dir = DirectoryManager()
        self.source = InvoiceSource(config)
        self.downloader = InvoiceDownloader(config)
        self.parser = InvoiceParser(config)
        # self.exporter = InvoiceExporter(config)

    def run(self):

        # Setup the environment and directories
        output_html_path = self.config.dir.output_html
        if os.path.exists(output_html_path):
            shutil.rmtree(output_html_path)
        os.makedirs(output_html_path, exist_ok=True)

        # Get the list of invoice NFCe codes from the source
        invoice_nfce_codes = self.source.run()
        invoice_nfce_codes = list(set(invoice_nfce_codes[0:2]))  # Remove duplicates

        # Scrap invoices from the source and download them
        for x, nfce_code in enumerate(invoice_nfce_codes):
            nfce_id = x + 1
            try:                
                self.logger.info(f"Processing nfce {nfce_id}/{len(invoice_nfce_codes)} with key: {nfce_code}")
                self.downloader.run(nfce_code, nfce_id)       
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")
                continue

        html_files = self.dir.list_files(self.config.dir.output_html, extension=".html")
        breakpoint()