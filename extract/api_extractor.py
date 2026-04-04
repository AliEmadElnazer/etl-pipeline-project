import requests
import pandas as pd
from datetime import datetime
import os


class APIExtractor:

    def __init__(self, app_id):
        self.app_id = app_id
        self.base_url = "https://openexchangerates.org/api/latest.json"

    def fetch_data(self):
        params = {"app_id": self.app_id}

        response = requests.get(self.base_url, params=params)

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code}")

        return response.json()

    def transform(self, data):
        rates = data["rates"]
        base = data["base"]
        
        df = pd.DataFrame(list(rates.items()), columns=["currency", "rate"])

        df["base_currency"] = base
        df["extraction_time"] = datetime.utcnow()
        df["source"] = "API"

        return df

    def save(self, df, path="data/raw/exchange_rates.csv"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)

    def run(self):
        print("Fetching API Data...")

        data = self.fetch_data()
        df = self.transform(data)
        self.save(df)

        print("API Extraction Done ✅")