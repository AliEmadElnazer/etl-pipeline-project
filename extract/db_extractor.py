import sqlite3
import pandas as pd
from datetime import datetime
import os


class DBExtractor:

    def __init__(self, db_path="data/orders.db"):
        self.db_path = db_path

    def extract_table(self, table_name):
        conn = sqlite3.connect(self.db_path)

        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)

        conn.close()

        return df

    def add_metadata(self, df):
        df["extraction_time"] = datetime.utcnow()
        df["source"] = "Database"
        return df

    def save(self, df, table_name):
        path = f"data/raw/{table_name}.csv"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)

    def run(self):
        print("📊 Extracting from Database...")

        tables = ["orders", "order_items"]

        for table in tables:
            df = self.extract_table(table)
            df = self.add_metadata(df)
            self.save(df, table)

        print("✅ Database Extraction Done")