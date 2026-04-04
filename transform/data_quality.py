import pandas as pd
import os


class DataQuality:

    def __init__(self, input_path="data/raw", output_path="data/staging_1"):
        self.input_path = input_path
        self.output_path = output_path

    def remove_duplicates(self, df):
        return df.drop_duplicates()

    def handle_nulls(self, df):
        # Forward fill null values (updated for new pandas versions)
        return df.ffill()

    def validate_data(self, df):
        # Validate price (no negative values)
        if "price" in df.columns:
            df = df[df["price"] >= 0]

        # Validate quantity (must be > 0)
        if "quantity" in df.columns:
            df = df[df["quantity"] > 0]

        return df

    def process_file(self, file_name):
        file_path = os.path.join(self.input_path, file_name)

        # Read file
        df = pd.read_csv(file_path)

        # Apply cleaning steps
        df = self.remove_duplicates(df)
        df = self.handle_nulls(df)
        df = self.validate_data(df)

        # Save cleaned data
        os.makedirs(self.output_path, exist_ok=True)
        output_path = os.path.join(self.output_path, file_name)
        df.to_csv(output_path, index=False)

    def run(self):
        print("🧹 Running Data Quality...")

        files = os.listdir(self.input_path)

        for file in files:
            if file.endswith(".csv"):
                self.process_file(file)

        print("Data Quality Done")