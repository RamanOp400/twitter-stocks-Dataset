import os 
import sys
import pandas as pd 
import joblib
import yaml
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error

from src.exception import CustomException
from src.logger import logggggg
from src.entity.artifact_entity import model_training_artifact, data_transformation_artifact
from src.entity.config_entity import model_trainer_config

logger = logggggg()

class Model_Training:
    """
    This class is responsible for managing the model training process, 
    evaluating the model, and saving the artifacts (model and YAML report).
    """
    # 1. Accept the receipt from the Data Transformation step
    def __init__(self, data_transformation_artifact: data_transformation_artifact):
        try:
            logger.info("Initializing Model_Training class.")

            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config()

            logger.info("Model_Training class initialized successfully.")
        except Exception as e:
            logger.error(f"Error while initializing Model_Training: {e}")
            raise CustomException(e, sys)
        
    def initiate_model_training(self) -> model_training_artifact:
        """
        Starts the model training and evaluation process, saves the model to a .pkl file,
        saves metrics to a .yaml file, and returns the training artifact.
        """
        try:
            logger.info("Starting model training process.")
            
            # 2. Extract paths exactly as they were spelled in the previous artifact (Capital X and Y)
            train_x_path = self.data_transformation_artifact.x_train_file_path
            test_x_path = self.data_transformation_artifact.x_test_file_path
            train_y_path = self.data_transformation_artifact.y_train_file_path
            test_y_path = self.data_transformation_artifact.y_test_file_path

            # Load the transformed data
            X_train = pd.read_csv(train_x_path)
            X_test = pd.read_csv(test_x_path)
            y_train = pd.read_csv(train_y_path).values.ravel() # .values.ravel() converts to 1D array for sklearn
            y_test = pd.read_csv(test_y_path).values.ravel()

            logger.info("Training data loaded successfully. Initializing RandomForestRegressor.")

            # Initialize and train the model
            model = RandomForestRegressor(
                n_estimators=700,
                max_depth=None,
                min_samples_leaf=4,
                max_features=0.8,
                random_state=42,
                n_jobs=-1
            )
            
            # Train and predict
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            logger.info("Model training completed. Calculating evaluation metrics.")

            # 3. Calculate metrics (changed variable names so they don't overwrite sklearn functions)
            calculated_r2 = r2_score(y_test, y_pred)
            calculated_rmse = root_mean_squared_error(y_test, y_pred)
            calculated_mae = mean_absolute_error(y_test, y_pred)

            evaluation_metrics = {
                "model_name": "RandomForestRegressor",
                "r2_score": float(calculated_r2),   # cast to float for clean YAML saving
                "rmse": float(calculated_rmse),
                "mae": float(calculated_mae)
            }
            
            logger.info(f"Model evaluation metrics: {evaluation_metrics}")

            # 4. Create directories for saving
            file_model_dir = self.model_trainer_config.model_file_path
            file_report_dir = self.model_trainer_config.model_training_expected_accuracy_file_path

            os.makedirs(file_model_dir, exist_ok=True)
            os.makedirs(file_report_dir, exist_ok=True)

            # 5. Save Model (.pkl) and Report (.yaml)
            model_save_path = os.path.join(file_model_dir, "model.pkl")
            report_save_path = os.path.join(file_report_dir, "metrics_report.yaml")

            joblib.dump(model, model_save_path)
            logger.info(f"Model saved at {model_save_path}")

            with open(report_save_path, "w") as file:
                yaml.dump(evaluation_metrics, file)
            logger.info(f"YAML metrics report saved at {report_save_path}")

            # 6. Hand the receipt to the final artifact
            artifact = model_training_artifact(
                model_save_file=model_save_path,
                evaluation_report=report_save_path,
            )
            
            return artifact
        
        except Exception as e:
            logger.error(f"Error during model training and evaluation: {e}")
            raise CustomException(e, sys)