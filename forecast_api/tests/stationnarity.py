from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from utils import StationnarityRequestBody

def get_stationnarity(request:StationnarityRequestBody) -> dict:
    values = request.values
    adf_results = adfuller(values)
    kpss_results = kpss(values)
    return {
        "ADF": {
                "ADF-stat":adf_results[0],
                "p-value":adf_results[1],
                "critical-values":adf_results[4]
            },
        "KPSS": {
                "KPSS-stat":kpss_results[0],
                "p-value":kpss_results[1],
                "critical-values":kpss_results[3]
        }
    }
        