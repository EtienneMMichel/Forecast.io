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

class StationnarityRequestBody(BaseModel):
    values:list[float]

class GrangerCausalityRequestBody(BaseModel):
    ref_ticket:str
    cause_tickets:list[str]
    start_date:str
    end_date:str
    timeframe:str | None = None
    data_type:str | None = None
    max_lags:int | None = None
    period:str | None = None
    