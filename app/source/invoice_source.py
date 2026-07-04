from app.utils.directory import DirectoryManager
from app.utils.file import FileManager
import logging
import os

class InvoiceSource:

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.file_manager = FileManager()
        self.directory_manager = DirectoryManager()

    def list_invoice_history_files(self):
        return self.directory_manager.list_files(self.config.dir.input)
    
    def get_invoice_history(self, file_list):
        history = []
        file = [x for x in file_list if str(self.config.year) in x][0]  # Get the first file that contains the year
        file_path = os.path.join(self.config.dir.input, file)
        contents = self.file_manager.read_csv(file_path)
        history.extend(contents[1])
        columns = contents[0]
        return history, columns
    
    def list_invoice_nfce_codes(self, history):
        return [row[6] for row in history]  # Assuming the first column contains the codes
    
    def save_invoice_history(self, history, columns):
        self.file_manager.save_csv(f"{self.config.dir.output}/invoice_history.csv", columns, history)


    def run(self):
        file_list = self.list_invoice_history_files()
        history, columns = self.get_invoice_history(file_list)
        self.save_invoice_history(history, columns)
        return self.list_invoice_nfce_codes(history)