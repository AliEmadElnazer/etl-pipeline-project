from extract.api_extractor import APIExtractor
from extract.db_extractor import DBExtractor
from extract.file_extractor import FileExtractor

API_KEY = "379aa3a3149d412d80d09d11b7a53442"

if __name__ == "__main__":
    print("ETL Started 🚀")

    # API
    api = APIExtractor(API_KEY)
    api.run()

    # DB
    db = DBExtractor()
    db.run()

    # Data Lake
    file_extractor = FileExtractor()
    file_extractor.run()