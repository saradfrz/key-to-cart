import os
import csv

class DataTools():
    def __init__(self):
        pass

    def get_all_data_files(self, folder, extension) -> list:
        """
        Get all files with the specified extension from the folder.
        Returns:
            list: A list of paths to all files with the specified extension in the folder and its subfolders.
        """

        files_with_extension = []
        for root, dirs, files in os.walk(folder):
            for filename in files:
                if filename.endswith(extension):
                    files_with_extension.append(os.path.join(root, filename))
        return files_with_extension

    def get_all_files_content(self, file_list, extension) -> list:
        """
        Read the content of all files with the specified extension and return a list of their contents.
        Args:
            file_list (list): A list of paths to files.
        Returns:
            list: A list containing the combined content of all files, as parsed by the appropriate method for the extension.
        """
        data = []
        for file in file_list:
            if file.endswith(extension):
                if extension == '.csv':
                    file_data = self._get_csv_content(file)
                    data.extend(file_data)
                elif extension == '.html':
                    file_data = self._get_html_content(file)
                    data.extend(file_data)
        return data
    
    def create_unique_key(self, access_key,  purchase_date, store_name) -> str:
        """
        Builds a normalized nfce filename in the format: YYYYMMDD__AccessKey__StoreName
        """
        access_key = access_key.replace(" ", "")

        # Format date as YYYYMMDD
        raw_date = purchase_date.strip()
        date_parts = raw_date.split("/")
        formatted_date = "".join(date_parts[::-1])  # DD/MM/YYYY → YYYYMMDD

        # Normalize store name for filesystem safety
        store_name = (
            store_name
            .strip()
            .replace(" ", "_")
            .replace("/", "")
            .replace("\\", "")
            .lower()
        )
        return f"{formatted_date}__{access_key}__{store_name}"

    def _get_csv_content(self, csv_file: str) -> list:
        """
        Read the content of a CSV file and return it as a list of dictionaries (one per row).
        Args:
            csv_file (str): Path to the CSV file.
        Returns:
            list: A list of dictionaries representing the rows in the CSV file, or an empty list if the file is empty.
        """
        
        with open(csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        return data if data else []
    
    def _get_html_content(self, html_file: str) -> list:
        """
        Read the content of an HTML file and return it as a string in a list (for consistency with CSV output).
        Args:
            html_file (str): Path to the HTML file.
        Returns:
            list: A list containing the HTML content as a single string, or an empty list if the file is empty.
        """
        with open(html_file, mode='r', encoding='utf-8') as f:
            content = f.read()
        return [content] if content else []