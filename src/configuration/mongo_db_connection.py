import pymongo
import os 
import certifi
import sys 
from src.exception import CustomException
from src.logger import logggggg
from src.constants import PROJECT_NAME,PROJECT_COLLECTION_NAME,DATA_INGESTION_URL

ca = certifi.where()

class MongoDBConnection:
    """
    A class to manage MongoDB connections.
    attributes :
        client (pymongo.MongoClient): The MongoDB client.
        db (pymongo.database.Database): The MongoDB database.
    """
    def __init__(self):
        """
        Initializes the MongoDBConnection class by establishing a connection to the MongoDB database.
        """
        try:
            if not DATA_INGESTION_URL:
                raise ValueError("MONGO_DB_KEYS is not set. Check the .env file or environment variables.")

            self.client = pymongo.MongoClient(DATA_INGESTION_URL, tlsCAFile=ca)
            self.db = self.client[PROJECT_NAME]
            self.collection = self.db[PROJECT_COLLECTION_NAME]
            logger = logggggg()
            logger.info("MongoDB connection established successfully.")
        except Exception as e:
            logger = logggggg()
            logger.error(f"Error while connecting to MongoDB: {e}")
            raise CustomException(e, sys)