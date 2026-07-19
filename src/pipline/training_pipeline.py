import sys 
import os 
from src.exception import CustomException
from src.logger import logggggg
from src.components.data_ingestion import DataIngestion_Raman
from src.entity.config_entity import (ingestion_config,data_validation_config,data_transformation_config)
from src.entity.artifact_entity import (instesgtion_artifact,data_validation_artifact,data_transformation_artifact)
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
# lets build and pipe line class uff this oops 

class TrainingPipeline:
    """
    A class to manage the training pipeline, including data ingestion and artifact creation.
    """
    def __init__(self):

        self.ingestion_config = ingestion_config()
        self.data_validation_config = data_validation_config()
        self.data_transformation_config = data_transformation_config()

    def start_data_ingestion(self) -> instesgtion_artifact:
        """
        Starts the data ingestion process and returns the ingestion artifact.

        Returns:
            instesgtion_artifact: The artifact containing information about the ingested data.
        """
        try:
            logger = logggggg()
            logger.info("Starting data ingestion process.")
            
            # Create an instance of DataIngestion_Raman with the ingestion configuration
            data_ingestion = DataIngestion_Raman(ingestion_config=self.ingestion_config)
            
            # Export data from MongoDB to feature store and get the artifact
            ingestion_artifact = data_ingestion.export_data_as_feature_store()
            
            logger.info("Data ingestion process completed successfully.")
            return ingestion_artifact
        
        except Exception as e:
            logger = logggggg()
            logger.error(f"Error during data ingestion: {e}")
            raise CustomException(e, sys)
    
    def start_data_validation(self) -> data_validation_artifact:
        """
        Starts the data validation process and returns the validation artifact.

        Returns:
            data_validation_artifact: The artifact containing information about the validated data.
        """
        try:
            logger = logggggg()
            logger.info("Starting data validation process.")
            
            # Create an instance of DataValidation with the validation configuration
            data_validation = DataValidation()
            
            # Run data validation and get the artifact
            validation_artifact = data_validation.run_validation_visualization2()
            
            logger.info("Data validation process completed successfully.")
            return validation_artifact

        except Exception as e:
            logger = logggggg()
            logger.error(f"Error during data validation: {e}")
            raise CustomException(e, sys)
        
    def start_data_transformation(self):

        """
        Starts the data transformation process and returns the transformation artifact.

        Returns:
            data_transformation_artifact: The artifact containing information about the transformed data.
        """

        try:
            logger = logggggg()
            logger.info("Starting data transformation process.")
            
            # Create an instance of DataTransformation with the transformation configuration
            data_transformation = DataTransformation()
            
            # Run data transformation and get the artifact
            transformation_artifact = data_transformation.run_data_trans()
            logger.info("Data transformation process completed successfully.")

            return transformation_artifact
        
        except Exception as e:
            logger = logggggg()
            logger.error(f"Error during data transformation: {e}")
            raise CustomException(e, sys)




    def run_pipeline(self):
        """
         Runs the entire training pipeline, including data ingestion and any subsequent steps.
        """
        try:
            logger = logggggg()
            logger.info("Starting the training pipeline.")
            
            # Start data ingestion and get the artifact
            ingestion_artifact = self.start_data_ingestion()
            
            # Start data validation and get the artifact
            validation_artifact = self.start_data_validation()

            # Start data transformation and get the artifact
            transformation_artifact = self.start_data_transformation()

            logger.info("Training pipeline completed successfully.")
        
        except Exception as e:
            logger = logggggg()
            logger.error(f"Error during training pipeline execution: {e}")
            raise CustomException(e, sys)