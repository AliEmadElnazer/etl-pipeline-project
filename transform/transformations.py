import pandas as pd
import os


class Transformation:

    def __init__(self, input_path="data/staging_1", output_path="data/staging_2"):
        self.input_path = input_path
        self.output_path = output_path

    # ---------------------------
    # Load Data
    # ---------------------------
    def load_data(self):
        self.products = pd.read_csv(f"{self.input_path}/products.csv")
        self.exchange_rates = pd.read_csv(f"{self.input_path}/exchange_rates.csv")

    # ---------------------------
    # Currency Conversion
    # ---------------------------
    def currency_conversion(self):
        egp_rate = self.exchange_rates[
            self.exchange_rates["currency"] == "EGP"
        ]["rate"].values[0]

        self.products["price_egp"] = self.products["list_price"] * egp_rate

    # ---------------------------
    # Load Orders Data
    # ---------------------------
    def load_additional_data(self):
        self.orders = pd.read_csv(f"{self.input_path}/orders.csv")
        self.order_items = pd.read_csv(f"{self.input_path}/order_items.csv")

    # ---------------------------
    # Merge Tables
    # ---------------------------
    def merge_tables(self):
        merged = self.order_items.merge(
            self.products, on="product_id", how="left"
        )

        merged = merged.merge(
            self.orders, on="order_id", how="left"
        )

        self.final_df = merged

    # ---------------------------
    # Clean Columns
    # ---------------------------
    def clean_columns(self):
        self.final_df.rename(columns={
            "list_price_x": "item_price",
            "list_price_y": "product_price"
        }, inplace=True)

        columns_to_drop = [
            "Extraction_Date_x", "Extraction_Date_y",
            "source_x", "source_y",
            "extraction_time_x", "extraction_time_y"
        ]

        self.final_df.drop(
            columns=[col for col in columns_to_drop if col in self.final_df.columns],
            inplace=True
        )

    # ---------------------------
    # Delivery Metrics
    # ---------------------------
    def delivery_metrics(self):
        self.final_df["order_date"] = pd.to_datetime(self.final_df["order_date"])
        self.final_df["shipped_date"] = pd.to_datetime(self.final_df["shipped_date"])

        self.final_df["latency_days"] = (
            self.final_df["shipped_date"] - self.final_df["order_date"]
        ).dt.days

        self.final_df["late_delivery"] = self.final_df["latency_days"] > 3

    # ---------------------------
    # Build Fact Table
    # ---------------------------
    def build_fact_table(self):
        self.fact_sales = self.final_df[[
            "order_id",
            "product_id",
            "customer_id",
            "store_id",
            "staff_id",
            "quantity",
            "price_egp",
            "discount",
            "latency_days",
            "late_delivery"
        ]]

    # ---------------------------
    # Build Product Dimension
    # ---------------------------
    def build_dim_product(self):
        self.dim_product = self.final_df[[
            "product_id",
            "product_name",
            "brand_id",
            "category_id",
            "model_year"
        ]].drop_duplicates()

    # ---------------------------
    # Save Outputs
    # ---------------------------
    def save_products(self):
        os.makedirs(self.output_path, exist_ok=True)
        self.products.to_csv(
            f"{self.output_path}/products_transformed.csv", index=False
        )

    def save_final(self):
        self.final_df.to_csv(
            f"{self.output_path}/sales_dataset.csv", index=False
        )

    def save_fact(self):
        self.fact_sales.to_csv(
            f"{self.output_path}/fact_sales.csv", index=False
        )

    def save_dim_product(self):
        self.dim_product.to_csv(
            f"{self.output_path}/dim_product.csv", index=False
        )

    # ---------------------------
    # Run Pipeline
    # ---------------------------
    def run(self):
        print("💱 Running Transformations...")

        # Load & transform products
        self.load_data()
        self.currency_conversion()

        # Load & merge orders
        self.load_additional_data()
        self.merge_tables()

        # Clean + metrics
        self.clean_columns()
        self.delivery_metrics()

        # Build tables
        self.build_fact_table()
        self.build_dim_product()

        # Save outputs
        self.save_products()
        self.save_final()
        self.save_fact()
        self.save_dim_product()

        print("✅ Transformations Done")