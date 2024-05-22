# Forecast.io
Forecasting app deployed on AWS 

## 1. training mode

### download dataset
modify yaml file training/scripts/download_data.yaml and run :

````bash
python training/scripts/get_data.py training/scripts/download_data.yaml
````

### train a model
modify yaml file training/scripts/config.yaml and run :

````bash
python training/main.py training/config.yaml train
````

## 2. Deploy API