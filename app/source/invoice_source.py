from app.utils.directory import DirectoryManager
from app.utils.file import FileManager
import logging

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
        for file in file_list:
            contents = self.file_manager.read_csv(file)
            history.extend(contents[1])
            columns = contents[0]  # Extend with rows, excluding header
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