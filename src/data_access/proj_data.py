import os 
import sys
from src.exception import CustomException
from src.logger import logggggg
from src.configuration.mongo_db_connection import MongoDBConnection
import pandas as pd
import numpy as np 

class DataAccess:
    """
    A class to manage data access operations, including reading and writing data to MongoDB.
    """

    def __init__(self):
        """
        Initializes the DataAccess class by establishing a connection to the MongoDB database.
        """
        try:
            self.mongo_connection = MongoDBConnection()
            self.collection = self.mongo_connection.collection
        except Exception as e:
            logger = logggggg()
            logger.error(f"Error while initializing DataAccess: {e}")
            raise CustomException(e, sys)
        
    def read_data(self,query:dict):
        """
        Reads data from the MongoDB collection based on the provided query.

        Args:
            query (dict): The query to filter the data.

        Returns:
            pandas.DataFrame: The filtered data as a DataFrame.
        """
        try:
            data = list(self.collection.find(query))
            df = pd.DataFrame(data)
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"])
            df.replace({"na":np.nan},inplace=True)

            return df 
            
        except Exception as e:
            logger = logggggg()
            logger.error(f"Error while reading data from MongoDB: {e}")
            raise CustomException(e, sys)
