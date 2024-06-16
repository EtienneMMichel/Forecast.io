from statsmodels.tsa.stattools import grangercausalitytests
from utils import GrangerCausalityRequestBody, GetDataRequestBody
from utils.dataloader import get_data_from_csv
import pandas as pd
from utils.timestamp import get_next_timestamp, MAPPING_PERIOD
from datetime import datetime

def get_granger_causality(request:GrangerCausalityRequestBody) -> dict:
    # Add a min max scaler to the data
    data_type = request.data_type if request.data_type else "close_returns"
    timeframe = request.timeframe if request.timeframe else "H1"
    max_lags = request.max_lags if request.max_lags else 4
    period = request.period if request.period else "D1"
    symbol_metadata_ref = f"{request.ref_ticket}_{timeframe}"
    start_date = request.start_date
    end_date = request.end_date

    nb_period = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S') - datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    nb_period = eval(f"nb_period.{MAPPING_PERIOD[period[0]]}")
    next_date = start_date
    res = {}
    for i in range(nb_period):
        end_next_date = get_next_timestamp(next_date, period, 1)[0]
        end_next_date = end_next_date.strftime('%Y-%m-%d %H:%M:%S')
        data = get_data_from_csv(GetDataRequestBody(symbol_metadata=[symbol_metadata_ref], start_date="2019-01-01", end_date="2021-01-01"))
        data = data[symbol_metadata_ref]
        data = pd.DataFrame(data)
        data = data.set_index("time")
        data = data[data_type].to_frame()
        data = data.dropna()
        current_day_cause = {}
        for cause_ticket in request.cause_tickets:
            symbol_metadata_cause = f"{cause_ticket}_{timeframe}"
            cause_data = get_data_from_csv(GetDataRequestBody(symbol_metadata=[symbol_metadata_cause], start_date="2019-01-01", end_date="2021-01-01"))
            cause_data = cause_data[symbol_metadata_cause]
            cause_data = pd.DataFrame(cause_data)
            cause_data = cause_data.set_index("time")
            cause_data = cause_data[data_type].to_frame()
            cause_data = cause_data.dropna()
            data = data.join(cause_data, how="inner", lsuffix=f"_{request.ref_ticket}", rsuffix=f"_{cause_ticket}")
            data = data.dropna()
            granger_results_raw = grangercausalitytests(data, max_lags, verbose=False)
            granger_results = {}
            for lag in granger_results_raw.keys():
                granger_results[int(lag)] = {
                    "ssr_ftest":{
                        "ftest": float(granger_results_raw[lag][0]["ssr_ftest"][0]),
                        "pvalue": float(granger_results_raw[lag][0]["ssr_ftest"][1]),
                    },
                    "ssr_chi2test": {
                        "ftest": float(granger_results_raw[lag][0]["ssr_chi2test"][0]),
                        "pvalue": float(granger_results_raw[lag][0]["ssr_chi2test"][1]),
                    },
                    "likelihood_ratio_test": {
                        "ftest": float(granger_results_raw[lag][0]["lrtest"][0]),
                        "pvalue": float(granger_results_raw[lag][0]["lrtest"][1]),
                    },
                    "params_ftest": {
                        "ftest": float(granger_results_raw[lag][0]["params_ftest"][0]),
                        "pvalue": float(granger_results_raw[lag][0]["params_ftest"][1]),
                    }
                } 
            current_day_cause[cause_ticket] = granger_results
        res[end_next_date] = current_day_cause
        next_date = end_next_date
    return res