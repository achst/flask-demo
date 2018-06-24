import datetime
import decimal


def serializer(data):
    if data is None:
        return None

    if isinstance(data, (tuple, list)):
        dicts = []
        for each in data:
            dicts.append(serializer(each))
        return dicts
    if not isinstance(data, dict):
        return data
    result_data = {}
    for key, value in data.items():
        if isinstance(value, (tuple, list, dict)):
            result_data[key] = serializer(value)
        elif isinstance(value, datetime.datetime):
            result_data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, datetime.date):
            result_data[key] = value.strftime("%Y-%m-%d")
        elif isinstance(value, datetime.time):
            result_data[key] = value.strftime("%H:%M:%S")
        elif isinstance(value, datetime.timedelta):
            result_data[key] = str(value)
        elif isinstance(value, decimal.Decimal):
            result_data[key] = str(value)
        else:
            result_data[key] = value
    return result_data
