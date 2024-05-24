import json
import logging
from fastapi import FastAPI
import uvicorn
from forecast_api.utils import build_pipeline
from utils import TrainingRequestBody, ForecastingRequestBody
from training.main import train


logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = FastAPI(root_path="/prod")


@app.get("/")
async def root() -> dict:
    """
    **Dummy endpoint that returns 'hello world' example.**

    ```
    Returns:
        dict: 'hello world' message.
    ```
    """
    return {"message": "Hello World"}


@app.post("/predict")
async def get_forecasting(request:ForecastingRequestBody) -> dict:
    """
    **Endpoint implementing the forecasting logic.**

    ```
    Args:
        inputs (str): Question to be answered. Answer should be included in 'context'.
        model_name (str): Context containing information necessary to answer 'question'.
    Returns:
        dict: Dictionary containing the answer to the question along with some metadata.
    ```
    """
    pipeline = build_pipeline(config_forecasting_model=request.config_forecasting_model, config_preprocess_model=request.config_preprocess_model, metadatas=request.data["metadatas"])
    pred = pipeline.predict(request.data)
    return {"prediction": pred.tolist()}

@app.post("/train")
async def train_model(request:TrainingRequestBody) -> dict:
    """
    **Endpoint implementing the training logic.**

    ```
    Args:
        inputs (str): Question to be answered. Answer should be included in 'context'.
        model_name (str): Name of the model to be used.
    Returns:
        dict: Dictionary containing the answer to the question along with some metadata.
    ```
    """

    train(json.loads(request.json()))

    return {"message": "Model trained successfully"}

if __name__ == "__main__":
    
    uvicorn.run("app:app", port=5000, log_level="info")