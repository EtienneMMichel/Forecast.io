from datetime import datetime, timedelta

MAPPING_PERIOD = {
    "D": "days",
    "H": "hours",
    "W": "weeks",
    "MN": "months"
}

def delta_timeframe(timeframe):
    if timeframe[0] == 'H':
        return timedelta(hours=int(timeframe[1:]))
    elif timeframe[0] == 'D':
        return timedelta(days=int(timeframe[1:]))
    elif timeframe == 'W1':
        return timedelta(weeks=1)
    elif timeframe == 'MN1':
        return timedelta(weeks=4)


def get_next_timestamp(current_timestamp, timeframe, prediction_lentgh):
    last_timestamp = datetime.strptime(current_timestamp, '%Y-%m-%d %H:%M:%S')
    delta = delta_timeframe(timeframe)
    return   [last_timestamp + (i+1)*delta for i in range(prediction_lentgh)]