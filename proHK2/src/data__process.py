import pandas as pd

def process_data(data):
    data['Order Date'] = pd.to_datetime(data['order_date'])
    data['Month'] = data['order_date'].dt.month
    data['Year'] = data['order_date'].dt.year
    data['Hour'] = data['order_date'].dt.hour
    return data.dropna()