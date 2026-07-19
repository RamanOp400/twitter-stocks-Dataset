import os 
import sys 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.exception import CustomException
from src.logger import logggggg
from src.entity.artifact_entity import data_validation_artifact
from src.entity.config_entity import data_validation_config
from src.data_access.proj_data import DataAccess

logger = logggggg()

class DataValidation:
    """
    A class to manage the data validation process, including reading data from MongoDB and validating it against specified criteria.
    """
    def __init__(self):
        try:
            logger.info("Initializing DataValidation class.")
            self.data_validation_config = data_validation_config()
            logger.info("DataValidation class initialized successfully.")
        except Exception as e:
            logger.error(f"Error while initializing DataValidation: {e}")
            raise CustomException(e, sys)
            
    def validate_data(self):
        """
        Validates data from MongoDB based on the provided validation criteria.
        """
        try:
            logger.info("Starting data validation process.")
            
            # Create an instance of DataAccess to read data from MongoDB
            data_access = DataAccess()
            logger.info("DataAccess instance created successfully.")
            
            # Read data from MongoDB
            df = data_access.read_data(query={})
            logger.info("Data read from MongoDB successfully.")

            # Perform validation checks
            df = df.drop(columns=['_id'], errors='ignore')
            df = df.drop_duplicates()
            df = df.dropna()  # Clean all dropped rows
            
            logger.info("Data validation completed successfully.")
            return df 
            
        except Exception as e:
            logger.error(f"Error while validating data: {e}")
            raise CustomException(e, sys)
    
    def run_validation_visualization1(self):
        """
        Runs the data validation process and returns the validated data.
        """
        try:
            logger.info("Fetching validated data for visualization.")
            validated_data = self.validate_data()
            return pd.DataFrame(validated_data)
        except Exception as e:
            logger.error(f"Error while fetching data for visualization: {e}")
            raise CustomException(e, sys)
        
    def run_validation_visualization2(self):
        """
        Runs the data visualization process and saves the plots.
        """
        df = self.run_validation_visualization1()
        plot_file = self.data_validation_config.validation_store_dir_name
        # Config paths
        plot_file1 = self.data_validation_config.validation_store_dir_name_1
        plot_file2 = self.data_validation_config.validation_store_dir_name_2 
        plot_file3 = self.data_validation_config.validation_store_dir_name_3

        # Create the actual directory where plots will be stored
        os.makedirs(os.path.join(plot_file), exist_ok=True)

        # ---------------------------------- PLOT 1 ----------------------------------
        try:
            logger.info("Generating Plot 1: Histograms.")
            fig, ax = plt.subplots(figsize=(15, 10), nrows=2, ncols=2)
            
            ax[0, 0].hist(df['Open'], bins=20, color='blue', alpha=0.7, linewidth=0.5, edgecolor='black')
            ax[0, 0].set_title('Distribution of Open Prices')
            ax[0, 0].set_xlabel('Open Price')

            ax[0, 1].hist(df['Low'], bins=20, color='green', alpha=0.7, linewidth=0.5, edgecolor='black')
            ax[0, 1].set_title('Distribution of Low Prices')
            ax[0, 1].set_xlabel('Low Price')

            ax[1, 0].hist(df['High'], bins=20, color='red', alpha=0.7, linewidth=0.5, edgecolor='black')
            ax[1, 0].set_title('Distribution of High Prices')
            ax[1, 0].set_xlabel('High Price')

            ax[1, 1].hist(df['Close'], bins=20, color='orange', alpha=0.7, linewidth=0.5, edgecolor='black')
            ax[1, 1].set_title('Distribution of Close Prices')
            ax[1, 1].set_xlabel('Close Price')

            plt.tight_layout()
            plt.savefig(plot_file1)
            plt.close() # FIXED: Clear memory
            
        except Exception as e:
            logger.error(f"Error in Plot 1: {e}")
            raise CustomException(e, sys)
            
        # ---------------------------------- PLOT 2 ----------------------------------
        try:
            logger.info("Generating Plot 2: Pairplot.")
            plt.figure(figsize=(15, 10))
            sns.pairplot(df[['Open', 'Low', 'High', 'Close']])
            plt.title('Pairplot of Open, Low, High, and Close Prices')
            plt.tight_layout()
            plt.savefig(plot_file2)
            plt.close() # FIXED: Clear memory
            
        except Exception as e:
            logger.error(f"Error in Plot 2: {e}")
            raise CustomException(e, sys)
        
        # ---------------------------------- PLOT 3 ----------------------------------
        try:
            logger.info("Generating Plot 3: Heatmap.")
            plt.figure(figsize=(10, 6))
            sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
            plt.title('Correlation Heatmap of Stock Prices')
            plt.tight_layout()
            plt.savefig(plot_file3)
            plt.close() # FIXED: Clear memory
            
        except Exception as e:
            logger.error(f"Error in Plot 3: {e}")
            raise CustomException(e, sys)

        # ---------------------------------- ARTIFACT --------------------------------
        logger.info("All plots saved. Returning artifact.")
        
        # You can adjust these variable names to match exactly what you wrote in artifact_entity.py
        artifact = data_validation_artifact(
            image_1_file_path=plot_file1,
            image_2_file_path=plot_file2,
            image_3_file_path=plot_file3
        )
        
        return artifact