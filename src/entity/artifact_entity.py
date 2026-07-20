from dataclasses import dataclass 

@dataclass 
class instesgtion_artifact:
    """
     Data ingestion artifact class to store the parameters required for data ingestion.

    """
    data_ingestion_directory_store : str

@dataclass
class data_validation_artifact:
    image_1_file_path: str
    image_2_file_path: str
    image_3_file_path: str

@dataclass
class data_transformation_artifact:
    """
     Data transformation artifact class to store the parameters required for data transformation.

    """
    x_train_file_path : str
    x_test_file_path : str
    y_train_file_path : str
    y_test_file_path : str


@dataclass 
class model_training_artifact:
    """
     Model training artifact class to store the parameters required for model training.

    """
    model_save_file : float
    evaluation_report : float

@dataclass
class model_prediction_report_artifact:
    """
     Model prediction report artifact class to store the parameters required for generating prediction reports.

    """
    saved_model_file_path_yaml : str