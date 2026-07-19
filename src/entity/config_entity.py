import os 
from datetime import datetime
from dataclasses import dataclass 
from src.constants import * 

Timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass 
class training_config:
    """
     Training configuration class to store the parameters required for training the model.

    """
    artifact_dir : str = os.path.join(ARTIFACT_DIR, Timestamp)
    

training_pipeline_config : training_config = training_config()


@dataclass

class ingestion_config:
    """
     Data ingestion configuration class to store the parameters required for data ingestion.

    """
    data_ingestion = os.path.join(training_pipeline_config.artifact_dir,DATA_INGESTION_DIR)
    data_name : str = DATA_INGESTION_COLLECTION_NAME
    data_ingestion_dir = os.path.join(data_ingestion, DATA_INGESTION_STORED_DIR)
    data_ingestion_file_path = os.path.join(data_ingestion_dir, DATA_INGESTION_CSV_FILE_NAME)

@dataclass
class data_validation_config:
    """
     Data validation configuration class to store the parameters required for data validation.

    """
    validation_store_dir_name = os.path.join(training_pipeline_config.artifact_dir, DATA_VALIDATION_STORED_DIR)
    validation_store_dir_name_1 = os.path.join(validation_store_dir_name, DATA_VALIDATION_STORED_DIR_1)
    validation_store_dir_name_2 = os.path.join(validation_store_dir_name, DATA_VALIDATION_STORED_DIR_2)
    validation_store_dir_name_3 = os.path.join(validation_store_dir_name, DATA_VALIDATION_STORED_DIR_3)

@dataclass
class data_transformation_config:
    """
     Data transformation configuration class to store the parameters required for data transformation.

    """
    data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR)
    data_transformation_train_file_path = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRAIN_FILE_NAME)
    data_transformation_test_file_path = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TEST_FILE_NAME)
    data_transformation_train_target_file_path = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRAIN_TARGET_FILE_NAME)
    data_transformation_test_target_file_path = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TEST_TARGET_FILE_NAME)

@dataclass 
class model_trainer_config:
    """
     Model training configuration class to store the parameters required for model training.

    """
    model_training_dir = os.path.join(training_pipeline_config.artifact_dir, MODEL_TRAINING_DIR)
    model_saved_dir = os.path.join(model_training_dir, MODEL_SAVED_DIR)
    model_file_path = os.path.join(model_saved_dir, MODEL_FILE_NAME)
    model_training_expected_accuracy = os.path.join(model_training_dir,MODEL_EVALUATION_DIR)
    model_training_expected_accuracy_file_path = os.path.join(model_training_expected_accuracy,MODEL_EVALUATION_REPORT_FILE_NAME)

