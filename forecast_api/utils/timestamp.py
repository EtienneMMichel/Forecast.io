from datetime import datetime, timedelta

MAPPING_PERIOD = {
    "D": "days",
    "H": "hours",
    "W": "weeks",
    "MN": "months"
}

def delta_timeframe(timeframe):
    if timeframe[0] == 'H':
        if timeframe[1] == '1':
            return timedelta(hours=1)
        elif timeframe[1] == '4':
            return timedelta(hours=4)
    elif timeframe[0] == 'D':
        if timeframe[1] == '1':
            return timedelta(days=1)
    elif timeframe == 'W1':
        return timedelta(weeks=1)
    elif timeframe == 'MN1':
        return timedelta(weeks=4)


def get_next_timestamp(current_timestamp, timeframe, prediction_lentgh):
    last_timestamp = datetime.strptime(current_timestamp, '%Y-%m-%d %H:%M:%S')
    delta = delta_timeframe(timeframe)
    return   [last_timestamp + (i+1)*delta for i in range(prediction_lentgh)]