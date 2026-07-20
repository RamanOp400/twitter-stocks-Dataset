import os
import sys
import shutil
import joblib

from src.exception import CustomException
from src.logger import logggggg
from src.entity.artifact_entity import model_training_artifact, model_prediction_report_artifact
from src.entity.config_entity import model_prediction_report_config

logger = logggggg()


class Model_Pusher:
    """
    This class is responsible for pushing the trained model to a known
    location inside the artifact directory so that the API server can
    load it without re-running the full training pipeline.
    """

    def __init__(self, model_training_artifact: model_training_artifact):
        try:
            logger.info("Initializing Model_Pusher class.")
            self.model_training_artifact = model_training_artifact
            self.model_pusher_config = model_prediction_report_config()
            logger.info("Model_Pusher class initialized successfully.")
        except Exception as e:
            logger.error(f"Error while initializing Model_Pusher: {e}")
            raise CustomException(e, sys)

    def push_model(self) -> model_prediction_report_artifact:
        """
        Copies the trained model to the model_pusher artifact directory
        so the FastAPI server can discover and load it.

        Returns:
            model_prediction_report_artifact: Artifact pointing to the pushed model path.
        """
        try:
            logger.info("Starting model pusher process.")

            # Source: the model saved during training
            source_model_path = self.model_training_artifact.model_save_file
            logger.info(f"Source model path: {source_model_path}")

            # Destination: model_pusher directory inside the artifact
            pusher_dir = self.model_pusher_config.model_prediction_report_dir
            os.makedirs(pusher_dir, exist_ok=True)

            dest_model_path = os.path.join(pusher_dir, "model.pkl")
            shutil.copy2(source_model_path, dest_model_path)
            logger.info(f"Model pushed to: {dest_model_path}")

            artifact = model_prediction_report_artifact(
                saved_model_file_path_yaml=dest_model_path
            )
            return artifact

        except Exception as e:
            logger.error(f"Error during model pusher process: {e}")
            raise CustomException(e, sys)
