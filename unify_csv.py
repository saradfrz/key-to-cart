import os
import glob
import pandas as pd
from typing import Optional, List

class CSVUnifier:
    def __init__(
        self,
        input_folder: str = "input/master_csv",
        output_file: str = "output/unified.csv",
        encoding: str = "utf-8",
        delimiter: str = ",",
        include_columns: Optional[List[str]] = None,
        sort_by: Optional[str] = None
    ):
        """
        Initialize the CSVUnifier class with configuration parameters.
        """
        self.input_folder = input_folder
        self.output_file = output_file
        self.encoding = encoding
        self.delimiter = delimiter
        self.include_columns = include_columns
        self.sort_by = sort_by

    def get_csv_files(self) -> List[str]:
        """
        Fetch all CSV file paths in the input folder.
        """
        pattern = os.path.join(self.input_folder, "*.csv")
        csv_files = glob.glob(pattern)
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {self.input_folder}")
        return csv_files

    def load_and_concat_csvs(self) -> pd.DataFrame:
        """
        Read and concatenate all CSVs in the folder.
        """
        dataframes = []
        for file in self.get_csv_files():
            df = pd.read_csv(file, encoding=self.encoding, delimiter=self.delimiter)
            if self.include_columns:
                df = df[self.include_columns]
            dataframes.append(df)
        combined_df = pd.concat(dataframes, ignore_index=True)
        if self.sort_by and self.sort_by in combined_df.columns:
            combined_df = combined_df.sort_values(by=self.sort_by)
        return combined_df

    def export_to_csv(self, df: pd.DataFrame):
        """
        Export the DataFrame to a single CSV file.
        """
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        df.to_csv(self.output_file, index=False, encoding=self.encoding)

    def run(self):
        """
        Execute the unification process.
        """
        df = self.load_and_concat_csvs()
        self.export_to_csv(df)
        print(f"Unified CSV saved to: {self.output_file}")

# ==== Execution Example ====
if __name__ == "__main__":
    # Configuration example - fully parameterized
    config = {
        "input_folder": "input/master_csv",
        "output_file": "output/unified.csv",
        "encoding": "utf-8",
        "delimiter": ",",
        "include_columns": None,   # Or for example: ["id", "name", "date"]
        "sort_by": None            # Or "date"
    }

    unifier = CSVUnifier(**config)
    unifier.run()
