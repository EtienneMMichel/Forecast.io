from pydantic import BaseModel

class ForecastingRequestBody(BaseModel):
    config_preprocess_model: dict | None = None
    config_forecasting_model: dict 
    data: dict


# ---------------------------------------------------

# class DatasetConfig(BaseModel):
#     name: str
#     nb_past_ticks: int
#     nb_next_ticks: int
#     DATA_DIR_PATH: str
#     symbols_metadata: list[str]

# class DataConfig(BaseModel):
#     trainpath: str
#     batch_size: int
#     num_workers: int
#     valid_ratio: float
#     dataset: DatasetConfig

# class ParamConfig(BaseModel):
#     lr: float
#     momentum: float | None = None
#     weight_decay: float | None = None

# class OptimConfig(BaseModel):
#     algo: str
#     params: ParamConfig

# class WandbConfig(BaseModel):
#     project: str
#     entity: str
# class LoggingConfig(BaseModel):
#     logdir:str
#     wandb: WandbConfig | None = None

# class ModelConfig(BaseModel):
#     name: str
#     hidden_size: int | None = None
#     num_layers: int | None = None
#     dropout: float | None = None
#     bidirectional: bool | None = None

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