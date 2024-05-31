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