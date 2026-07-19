import os 
import sys 
from src.exception import CustomException
from src.logger import logggggg
from src.data_access.proj_data import DataAccess
from src.entity.artifact_entity import instesgtion_artifact
from src.entity.config_entity import ingestion_config
from pandas import DataFrame



class DataIngestion_Raman:
    """
    what to do know i am bore lets me see  :
    A class to manage the data ingestion process, including reading data from MongoDB and saving it to a specified directory.
    lets goo ;
    Attributes:
        data_access (DataAccess): An instance of the DataAccess class for MongoDB operations.
        ingestion_config (ingestion_config): An instance of the ingestion_config class containing configuration parameters.
        ingestion_artifact (instesgtion_artifact): An instance of the instesgtion_artifact class to store ingestion parameters.   
    """
    def __init__(self,ingestion_config: ingestion_config = ingestion_config()):
        """
        Initializes the DataIngestion_Raman class with the provided ingestion configuration.
        """
        try:

            self.ingestion_config = ingestion_config 

        except Exception as e : 
            logger = logggggg()
            logger.error(f"Error while initializing DataIngestion_Raman: {e}")
            raise CustomException(e, sys)
    def export_data_as_feature_store(self):
        """
        Exports data from MongoDB to a specified feature store directory as a CSV file.
        """
        try:
            logger = logggggg()
            logger.info("Starting data export from MongoDB to feature store.")
            
            # Create an instance of DataAccess to read data from MongoDB
            data_access = DataAccess()
            
            # Read data from MongoDB
            df: DataFrame = data_access.read_data(query={})
            
            # Ensure the feature store directory exists
            feature_store_dir = self.ingestion_config.data_ingestion_dir
            os.makedirs(feature_store_dir, exist_ok=True)
            df = df.drop(columns=['_id'], errors='ignore')
            df = df.drop_duplicates()
            df = df.dropna()  # this gonnal clen all the dropn 
            df.to_csv(self.ingestion_config.data_ingestion_file_path, index=False)

            artifact = instesgtion_artifact(
                data_ingestion_directory_store=feature_store_dir
            )
            logger.info("Data export completed successfully.")
            return artifact
        except Exception as e:
            logger = logggggg()
            logger.error(f"Error while exporting data: {e}")
            raise CustomException(e, sys)
    
