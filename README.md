# training

## download dataset
modify yaml file training/scripts/download_data.yaml and run :

````bash
python training/scripts/get_data.py training/scripts/download_data.yaml
````

## training model
modify yaml file training/scripts/config.yaml and run :

````bash
python training/main.py training/config_template.yaml train
````