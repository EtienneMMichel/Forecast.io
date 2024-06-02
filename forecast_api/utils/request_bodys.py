from pydantic import BaseModel

class ForecastingRequestBody(BaseModel):
    config_preprocess_model: dict | None = None
    config_forecasting_model: dict 
    data: dict

class TrainingRequestBody(BaseModel):
    save_model_summary: bool
    data: dict
    optim: dict
    nepochs: int
    loss: str
    logging: dict
    model: dict

class GetDataRequestBody(BaseModel):
    symbol_metadata: list[str]
    start_date: str
    end_date: str


class BacktestingRequest(BaseModel):
    data_config: dict
    config_model: dict