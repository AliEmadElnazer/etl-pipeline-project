import os

# Extract
from extract.api_extractor import APIExtractor
from extract.db_extractor import DBExtractor
from extract.file_extractor import FileExtractor

# Data Quality
from transform.data_quality import DataQuality

# Transform
from transform.transformations import Transformation

# Load to Data Warehouse
from load.load_to_dw import DataWarehouseLoader


API_KEY = "379aa3a3149d412d80d09d11b7a53442"


if __name__ == "__main__":
    print("ETL Started 🚀")

    # ---------------------------
    # Extract
    # ---------------------------
    print("📡 Fetching API Data...")
    APIExtractor(API_KEY).run()
    print("API Extraction Done ✅")

    print("📊 Extracting from Database...")
    DBExtractor().run()
    print("Database Extraction Done ✅")

    print("📂 Extracting Data Lake Files...")
    FileExtractor().run()
    print("Data Lake Extraction Done ✅")

    # ---------------------------
    # Data Quality
    # ---------------------------
    print("🧹 Running Data Quality...")
    DataQuality().run()
    print("Data Quality Done ✅")

    # ---------------------------
    # Transform
    # ---------------------------
    print("💱 Running Transformations...")
    Transformation().run()
    print("Transformations Done ✅")

    # ---------------------------
    # Load to Data Warehouse
    # ---------------------------
    print("🏢 Loading Data Warehouse...")
    DataWarehouseLoader().run()
    print("Data Warehouse Loaded ✅")

    print("🎉 ETL Pipeline Completed Successfully!")