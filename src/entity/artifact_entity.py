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