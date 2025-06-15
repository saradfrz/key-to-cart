import os
import csv

class DataPrepForScraper():
    def __init__(self, csv_folder):
        self.csv_folder = csv_folder

    def get_all_data_files(self) -> list:
        """
        Get all CSV files from the specified folder.
        Returns:
        list: A list of paths to all CSV files in the folder.
        """

        csv_files = []
        for root, dirs, files in os.walk(self.csv_folder):
            for filename in files:
                if filename.endswith(".csv"):
                    csv_files.append(os.path.join(root, filename))
        return csv_files
    
    def get_all_files_content(self, csv_list) -> list:
        """
        Read the content of all CSV files and return a list of their contents.
        Args:
        csv_list (list): A list of paths to CSV files.
        """
        data = []
        for csv_file in csv_list:
            file_data = self._get_csv_content(csv_file)
            data.extend(file_data)
        return data

    def _get_csv_content(self, csv_file: str) -> list:
        """
        Read the content of a CSV file and return it as a list of dictionaries.
        Args:
        csv_file (str): Path to the CSV file.
        Returns:
        list: A list of dictionaries representing the rows in the CSV file.
        """
        
        with open(csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        return data if data else []