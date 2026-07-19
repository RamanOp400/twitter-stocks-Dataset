from datetime import date
import os
from pathlib import Path


def _load_env_file() -> None:
	env_path = Path(__file__).resolve().parents[2] / ".env"
	if not env_path.exists():
		return

	with env_path.open("r", encoding="utf-8") as env_file:
		for raw_line in env_file:
			line = raw_line.strip()
			if not line or line.startswith("#") or "=" not in line:
				continue

			key, value = line.split("=", 1)
			key = key.strip()
			value = value.strip().strip('"').strip("'")
			os.environ.setdefault(key, value)


_load_env_file()

# MONGO DB PARAMETERS 
PROJECT_NAME = "twitterSTock"
PROJECT_COLLECTION_NAME = "twitterSTockCollection"
DATA_INGESTION_URL = os.getenv("MONGO_DB_KEYS")

# few know things thats gona required 
DATA_INGESTION_CSV_FILE_NAME : str = "twitterstocks.csv" 


ARTIFACT_DIR : str = "artifact"

# ----------------------------------------
# DATA INGESTION PRAMETERS 
#----------------------------------------
DATA_INGESTION_DIR : str = "data_ingestion"
DATA_INGESTION_STORED_DIR : str = "data_ingestion_stored"

DATA_INGESTION_COLLECTION_NAME = "twitter-STock.CSV"

#-------------------------------------------------------
# DATA VALIDATION PARAMETERS
#-------------------------------------------------------
DATA_VALIDATION_DIR : str = "data_validation"
DATA_VALIDATION_STORED_DIR : str = "data_validation_stored"
DATA_VALIDATION_STORED_DIR_1 : str = "data_validation_stored_1.png" 
DATA_VALIDATION_STORED_DIR_2 : str = "data_validation_stored_2.png"
DATA_VALIDATION_STORED_DIR_3 : str = "data_validation_stored_3.png"


# -------------------------------------------------------
# DATA TRANSFORMATION PARAMETERS
# -------------------------------------------------------
DATA_TRANSFORMATION_DIR : str = "data_transformation"
DATA_TRANSFORMATION_TRAIN_FILE_NAME : str = "X_train.csv"
DATA_TRANSFORMATION_TEST_FILE_NAME : str = "X_test.csv"
DATA_TRANSFORMATION_TRAIN_TARGET_FILE_NAME : str = "Y_train.csv"
DATA_TRANSFORMATION_TEST_TARGET_FILE_NAME : str = "Y_test.csv"


# -------------------------------------------------------
# MODEL TRAINING PARAMETERS AND EVALUATION PARAMETERS
# -------------------------------------------------------
MODEL_TRAINING_DIR : str = "model_training"
MODEL_SAVED_DIR : str = "model_saved"
MODEL_FILE_NAME : str = "model.pkl"
MODEL_EVALUATION_DIR : str = "model_evaluation"
MODEL_EVALUATION_REPORT_FILE_NAME : str = "model_evaluation_report.yaml"
