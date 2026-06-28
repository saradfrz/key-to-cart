
import logging

from app.source.invoice_source import InvoiceSource
from app.downloader.invoice_downloader import InvoiceDownloader 
# from app.parser.invoice_parser import InvoiceParser
# from app.exporter.invoice_exporter import InvoiceExporter

class InvoicePipeline:

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.source = InvoiceSource(config)
        self.downloader = InvoiceDownloader(config)
        # self.parser = InvoiceParser(config)
        # self.exporter = InvoiceExporter(config)

    def run(self):

        invoice_nfce_codes = self.source.run()

        invoice_nfce_codes = list(set(invoice_nfce_codes[0:5]))  # Remove duplicates

        for x, nfce_code in enumerate(invoice_nfce_codes):
            try:
                id = x + 1
                self.logger.info(f"Processing nfce {id}/{len(invoice_nfce_codes)} with key: {nfce_code}")
                self.downloader.run(nfce_code)       
            except Exception as e:
                self.logger.error(f"An error occurred: {e}")
                continue

        breakpoint = 1  # Placeholder for potential future use

        # results = self.parser.parse_folder()

        # self.exporter.export(results)