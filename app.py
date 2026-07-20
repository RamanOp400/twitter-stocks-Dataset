import os
import sys
import glob
import yaml
import numpy as np
import pandas as pd
import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.exception import CustomException
from src.logger import logggggg

logger = logggggg()

app = FastAPI(title="Twitter Stocks Prediction API")


# -------------------- Pydantic Input Schema --------------------
class InputData(BaseModel):
    """
    Pydantic model for input data validation.
    Volume is NOT included because it is the prediction target.
    """
    Date: str = Field(..., description="Stock date (e.g. '2013-11-07')")
    Open: float = Field(..., description="Stock open price")
    High: float = Field(..., description="Stock high price")
    Low: float = Field(..., description="Stock low price")
    Close: float = Field(..., description="Stock close price")


# -------------------- Helper: find latest model --------------------
def _find_latest_model() -> str:
    """
    Scans the artifact/ directory for the most recent timestamp folder
    and returns the path to the pushed model.pkl inside model_pusher/.
    Falls back to searching inside model_training/ if model_pusher/ copy
    is not found.
    """
    artifact_root = os.path.join(os.path.dirname(__file__), "artifact")
    timestamp_dirs = sorted(glob.glob(os.path.join(artifact_root, "*")), reverse=True)

    for ts_dir in timestamp_dirs:
        # First try the pushed model location
        pusher_model = os.path.join(ts_dir, "model_pusher", "model.pkl")
        if os.path.isfile(pusher_model):
            return pusher_model

        # Fallback: search inside model_training
        model_candidates = glob.glob(
            os.path.join(ts_dir, "model_training", "model_saved", "**", "model.pkl"),
            recursive=True,
        )
        if model_candidates:
            return model_candidates[0]

    raise FileNotFoundError("No trained model found in the artifact/ directory. Run the training pipeline first.")


# -------------------- API Endpoint --------------------
@app.post("/predict")
def predict(input_data: InputData):
    """
    API endpoint to make predictions using the trained model.
    Accepts Date, Open, High, Low, Close — predicts Volume.
    Also saves the prediction report as a YAML file.

    Args:
        input_data (InputData): Input data for prediction.

    Returns:
        dict: Prediction result with the predicted volume.
    """
    try:
        # Load the latest trained model
        model_path = _find_latest_model()
        model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")

        # Convert input data to DataFrame
        input_dict = input_data.dict()
        # Add a placeholder Volume so the preprocessing pipeline can compute log_volume features
        # (the model was trained with lagged volume features, but for a single-row prediction
        #  these will all be NaN anyway — the model handles it)
        input_dict["Volume"] = 0.0
        df = pd.DataFrame([input_dict])

        logger.info("DATA PREPROCESSING STARTED")
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

        feature_prefixes = (
            'volume_lag_', 'return_lag_', 'log_close_lag_', 'volume_mean_',
            'volume_std_', 'return_std_', 'close_vs_ma_'
        )
        features = [column for column in df.columns if column.startswith(feature_prefixes)]
        features += ['prev_day_range_pct', 'day_of_week', 'month']

        # Extract ONLY the features needed, grabbing the final row to predict
        processed_features = df[features].iloc[-1:]

        # Make prediction
        prediction = model.predict(processed_features)
        real_volume = np.expm1(prediction)

        logger.info("Prediction successful. Returning decoded volume.")

        # --------- Save prediction report as YAML ---------
        report_dir = os.path.join(os.path.dirname(model_path))
        report_file_path = os.path.join(report_dir, "model_prediction_report.yaml")

        yaml_content = {
            "input_data": input_data.dict(),
            "predicted_volume": real_volume.tolist(),
        }
        with open(report_file_path, "w") as f:
            yaml.dump(yaml_content, f)

        logger.info(f"Model prediction report saved at: {report_file_path}")

        return {"predicted_volume": real_volume.tolist()}
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise CustomException(e, sys)
