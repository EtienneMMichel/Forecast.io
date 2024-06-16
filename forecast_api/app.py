import json
import logging
from fastapi import FastAPI
import uvicorn
from utils import build_pipeline
from utils import TrainingRequestBody, ForecastingRequestBody, GetDataRequestBody, BacktestingRequest, StationnarityRequestBody
from training.main import train
from training.backtesting import backtesting
from models.utils_model import register_all_models, get_registery

from tests.stationnarity import get_stationnarity

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = FastAPI(root_path="/prod")
# register_all_models()


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

@app.get("/get_data_infos")
async def get_data_infos() -> dict:
    """
    **read metadata .txt files located in ./training/DATA/metadatas**

    ```
    Returns:
        dict: Dictionary containing the metadatas of the datasets.
    ```
    """

    return {"message": "Model trained successfully"}


@app.post("/get_data")
async def get_data(request:GetDataRequestBody) -> dict:
    """
    **read metadata .txt files located in ./training/DATA/metadatas**

    ```
    Returns:
        dict: Dictionary containing the metadatas of the datasets.
    ```
    """
    def get_data(request):
        # get data from the API
        import pandas as pd

        res = {}
        for symbol_metadata in request.symbol_metadata:
            data = pd.read_csv(f"./training/DATA/{symbol_metadata}.csv")
            data = data.loc[(data["time"] >= request.start_date) & (data["time"] <= request.end_date)]
            data["close_returns"] = (data.close - data.close.shift(1))/data.close.shift(1)
            res[symbol_metadata] = data.to_dict(orient="records")
        return res
    
    data = get_data(request)
    return {"data": data}


# @app.post("/backtesting")
# async def backtesting(request: BacktestingRequest) -> dict:
#     backtesting(request.model_config, request.data_config)

@app.get("/get_models_registery")
async def get_models_registery() -> dict:
    return get_registery()


@app.post("/stationnarity")
async def stationnarity(request:StationnarityRequestBody) -> dict:
    return get_stationnarity(request)

if __name__ == "__main__":
    
    uvicorn.run("app:app", port=5000, log_level="info")