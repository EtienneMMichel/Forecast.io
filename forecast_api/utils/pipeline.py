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