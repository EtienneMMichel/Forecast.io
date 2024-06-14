

def backtesting(model_config, data_config):

    model = eval(f"forecasting.{model_config['name']}(model_config, input_size, output_size)")
    