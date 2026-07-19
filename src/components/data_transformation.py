import os 
import sys 
from src.exception import CustomException
from src.logger import logggggg
from src.entity.artifact_entity import data_transformation_artifact
from src.entity.config_entity import data_transformation_config
from src.data_access.proj_data import DataAccess
from src.components.data_validation import DataValidation
import pandas as pd
import numpy as np
logger = logggggg()

class DataTransformation:
    """
    A class to manage the data transformation process, including reading data from MongoDB and transforming it for training and testing.
    """
    def __init__(self):
        try:
            logger.info("Initializing DataTransformation class.")
            self.data_transformation_config = data_transformation_config()
            self.data_validation = DataValidation()
            logger.info("DataTransformation class initialized successfully.")
        except Exception as e:
            logger.error(f"Error while initializing DataTransformation: {e}")
            raise CustomException(e, sys)
    def run_data_trans(self):
        """
        Runs the data transformation process, including reading data from MongoDB, transforming it, and saving the transformed data to specified file paths.
        """
        try:
            logger.info("Starting data transformation process.")
            
            # Read validated data
            df = self.data_validation.validate_data()
            logger.info("Validated data read successfully.")

            # Split the data into training and testing sets
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date').copy()

            df['log_volume'] = np.log1p(df['Volume'])

            for lag in [1, 2, 3, 5, 10, 20, 60]:
               df[f'volume_lag_{lag}'] = df['log_volume'].shift(lag)
               df[f'return_lag_{lag}'] = df['Close'].pct_change(lag).shift(1)
               df[f'log_close_lag_{lag}'] = np.log(df['Close']).shift(lag)

            df['prev_day_range_pct'] = ((df['High'] - df['Low']) / df['Open']).shift(1)
            previous_return = df['Close'].pct_change().shift(1)

            for window in [3, 5, 10, 20, 60]:
                df[f'volume_mean_{window}'] = df['log_volume'].shift(1).rolling(window).mean()
                df[f'volume_std_{window}'] = df['log_volume'].shift(1).rolling(window).std()
                df[f'return_std_{window}'] = previous_return.rolling(window).std()
                df[f'close_vs_ma_{window}'] = (
                df['Close'].shift(1) / df['Close'].shift(1).rolling(window).mean() - 1
               )

            df['day_of_week'] = df['Date'].dt.dayofweek
            df['month'] = df['Date'].dt.month

            model_df = df.dropna()

            feature_prefixes = (
                    'volume_lag_', 'return_lag_', 'log_close_lag_', 'volume_mean_',
                    'volume_std_', 'return_std_', 'close_vs_ma_')
            features = [column for column in df.columns if column.startswith(feature_prefixes)]
            features += ['prev_day_range_pct', 'day_of_week', 'month']

            X = model_df[features]
            y = model_df['log_volume']

            logger.info("Data transformation completed successfully. Splitting into training and testing sets.")

            split = int(len(model_df) * 0.8)
            X_train, X_test = X.iloc[:split], X.iloc[split:]
            y_train, y_test = y.iloc[:split], y.iloc[split:]

            logger.info(f"Training set size: {len(X_train)}, Testing set size: {len(X_test)}")
            file_paths = os.path.join(self.data_transformation_config.data_transformation_dir)
            os.makedirs(file_paths, exist_ok=True)
            logger.info(f"Saving transformed data to {file_paths}.")

            X_train.to_csv(self.data_transformation_config.data_transformation_train_file_path, index=False, header=True)
            X_test.to_csv(self.data_transformation_config.data_transformation_test_file_path, index=False, header=True)
            y_train.to_csv(self.data_transformation_config.data_transformation_train_target_file_path, index=False, header=True)
            y_test.to_csv(self.data_transformation_config.data_transformation_test_target_file_path, index=False, header=True)

            artifact = data_transformation_artifact(
                x_train_file_path=self.data_transformation_config.data_transformation_train_file_path,
                x_test_file_path=self.data_transformation_config.data_transformation_test_file_path,
                y_train_file_path=self.data_transformation_config.data_transformation_train_target_file_path,
                y_test_file_path=self.data_transformation_config.data_transformation_test_target_file_path
            )
            logger.info("Data transformation artifact created successfully.")
            return artifact
        except Exception as e:
            logger.error(f"Error during data transformation: {e}")
            raise CustomException(e, sys)