from extract.api_extractor import APIExtractor
from extract.db_extractor import DBExtractor
from extract.file_extractor import FileExtractor
from transform.data_quality import DataQuality
from transform.transformations import Transformation    

API_KEY = "379aa3a3149d412d80d09d11b7a53442"

if __name__ == "__main__":
    print("ETL Started ")

    # Extract
    APIExtractor(API_KEY).run()
    DBExtractor().run()
    FileExtractor().run()

    # Data Quality
    DataQuality().run()

    # Transform
    Transformation().run()