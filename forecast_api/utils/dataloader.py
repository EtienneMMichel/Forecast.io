from .request_bodys import GetDataRequestBody

def get_data_from_csv(request: GetDataRequestBody) -> dict:
        # get data from the API
        import pandas as pd

        res = {}
        for symbol_metadata in request.symbol_metadata:
            data = pd.read_csv(f"./training/DATA/{symbol_metadata}.csv")
            data = data.loc[(data["time"] >= request.start_date) & (data["time"] <= request.end_date)]
            data["close_returns"] = (data.close - data.close.shift(1))/data.close.shift(1)
            res[symbol_metadata] = data.to_dict(orient="records")
        return res