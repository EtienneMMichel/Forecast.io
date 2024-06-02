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






import forecast_api.forecasting as forecasting
import forecast_api.preprocessing as preprocessing
import torch

class Pipeline:

    def __init__(self, forecasting_model, preprocess_model) -> None:
        self.forecasting_model = forecasting_model
        self.preprocess_model = preprocess_model

    def predict(self, data):
        x = torch.tensor(data["inputs"], dtype=torch.float32)
        if self.preprocess_model is not None:
            x = self.preprocess_model(x)
        return self.forecasting_model(x)


def build_pipeline(config_forecasting_model: dict = None, config_preprocess_model: dict = None, metadatas : dict = None) -> Pipeline:
    """
    **Builds the pipeline for the specified model.**
    
    ```
    Args:
        model_name (str): Name of the model to be built.
        preprocess_model_name (str): Name of the preprocessing model to be built.
    Returns:
        object: Model object.
    ```
    """

    forecasting_model = eval(f"forecasting.{config_forecasting_model['name']}(config_forecasting_model, metadatas['input_size'], metadatas['output_size'])")
    preprocess_model = None
    if config_preprocess_model is not None:
        preprocess_model = eval(f"preprocessing.{config_preprocess_model['name']}(config_preprocess_model)")

    return Pipeline(forecasting_model, preprocess_model) 