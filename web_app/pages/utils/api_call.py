import requests
import json


API_GATEWAY = "http://127.0.0.1:5000"

def get_data(symbols_metadata, start_date, end_date):
    

    url = f"{API_GATEWAY}/get_data"

    payload = json.dumps({
    "symbol_metadata": symbols_metadata,
    "start_date": start_date,
    "end_date": end_date
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)['data']

def predict(inputs, model_name:str, indices_to_predict:list, prediction_length:int):

    url = f"{API_GATEWAY}/predict"

    payload = json.dumps({
        "config_forecasting_model": {
            "name": model_name
        },
        "data": {
            "inputs": inputs,
            "metadatas": {
            "input_size": [len(inputs), len(inputs[0])],
            "output_size": [
                prediction_length,
                len(indices_to_predict)
            ]
            }
        }
        })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)['prediction']



def get_stationnarity(inputs:dict):

    url = f"{API_GATEWAY}/stationnarity"

    payload = json.dumps(inputs)
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)
