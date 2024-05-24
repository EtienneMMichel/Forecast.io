import yaml
import sys
from datetime import datetime
import MetaTrader5 as mt5
import pytz
import pandas as pd

SAVING_PATH = "training/DATA"

def download_data(symbol, timeframe, start, end):
    rates = mt5.copy_rates_range(symbol, eval(f"mt5.TIMEFRAME_{timeframe}"), start, end)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    rates_frame.to_csv(f"{SAVING_PATH}/{symbol}_{timeframe}.csv", index=False)

if __name__ == "__main__":
    config = yaml.safe_load(open(sys.argv[1], "r"))
    if not mt5.initialize():
        print("initialize () a échoué, code d'erreur =",mt5.last_error())
        quit()

    utc_from = datetime.strptime(config["utc_from"], '%m/%d/%y %H:%M:%S')
    utc_to = datetime.strptime(config["utc_to"], '%m/%d/%y %H:%M:%S')

    for symbol in config["symbols"]:
        for timeframe in config["timeframes"]:
            download_data(symbol, timeframe,utc_from, utc_to)

    mt5.shutdown()