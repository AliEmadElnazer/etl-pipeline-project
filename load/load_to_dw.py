import pandas as pd
import sqlite3
import os

class DataWarehouseLoader:

    def __init__(self, input_path="data/staging_2", db_path="data/orders.db"):
        self.input_path = input_path
        self.db_path = db_path

    def load_data(self):
        self.df = pd.read_csv(f"{self.input_path}/sales_dataset.csv")

    def create_connection(self):
        self.conn = sqlite3.connect(self.db_path)

    def create_dimensions(self):
        # Dim Product
        dim_product = self.df[[
            "product_id", "product_name", "brand_id", "category_id"
        ]].drop_duplicates()

        dim_product.to_sql("dim_product", self.conn, if_exists="replace", index=False)

        # Dim Customer
        dim_customer = self.df[["customer_id"]].drop_duplicates()
        dim_customer.to_sql("dim_customer", self.conn, if_exists="replace", index=False)

        # Dim Store
        dim_store = self.df[["store_id"]].drop_duplicates()
        dim_store.to_sql("dim_store", self.conn, if_exists="replace", index=False)

    def create_fact_table(self):
        fact_sales = self.df[[
            "order_id", "product_id", "customer_id",
            "store_id", "price_egp", "quantity",
            "late_delivery"
        ]]

        fact_sales.to_sql("fact_sales", self.conn, if_exists="replace", index=False)

    def run(self):
        print("🏢 Loading Data Warehouse...")

        self.load_data()
        self.create_connection()
        self.create_dimensions()
        self.create_fact_table()

        self.conn.close()

        print("✅ Data Warehouse Loaded")