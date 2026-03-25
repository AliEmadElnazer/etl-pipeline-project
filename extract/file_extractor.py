import pandas as pd
import os
from datetime import datetime


class FileExtractor:

    def __init__(self, input_path="data/source_datalake", output_path="data/raw"):
        self.input_path = input_path
        self.output_path = output_path

    def extract_file(self, file_name):
        file_path = os.path.join(self.input_path, file_name)

        df = pd.read_csv(file_path)

        # metadata
        df["extraction_time"] = datetime.utcnow()
        df["source"] = "DataLake"

        return df

    def save(self, df, file_name):
        path = os.path.join(self.output_path, file_name)
        os.makedirs(self.output_path, exist_ok=True)
        df.to_csv(path, index=False)

    def run(self):
        print("📂 Extracting Data Lake Files...")

        files = os.listdir(self.input_path)

        for file in files:
            if file.endswith(".csv"):
                df = self.extract_file(file)
                self.save(df, file)

        print("✅ Data Lake Extraction Done")