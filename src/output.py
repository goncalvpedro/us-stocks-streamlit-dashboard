import pandas as pd
from api import yf_api

initial_data = [
    {'symbol': 'SGOV', 'shares': 4.565, 'price': 100.49, 'first_acquisition': '2024-10-03'},
    {'symbol': 'STAG', 'shares': 6.211, 'price': 34.62, 'first_acquisition': '2024-10-02'},
    {'symbol': 'SPG', 'shares': 1.344, 'price': 160.00, 'first_acquisition': '2024-10-08'},
    {'symbol': 'O', 'shares': 2.960, 'price': 57.10, 'first_acquisition': '2024-10-03'},
    {'symbol': 'SPY', 'shares': 0.334, 'price': 547.46, 'first_acquisition': '2024-10-03'},
    {'symbol': 'INDA', 'shares': 2.018, 'price': 51.15, 'first_acquisition': '2024-10-03'},
    {'symbol': 'FXI', 'shares': 3.796, 'price': 30.38, 'first_acquisition': '2024-10-03'},
]
OUTPUT_DIR = r'output/'

for ticker in initial_data:

    historical_data = yf_api.get_historical_data(ticker['symbol'], ticker['first_acquisition'])
    dividends = yf_api.get_dividends(ticker['symbol'])
    info = yf_api.get_ticker_info(ticker['symbol'])

    historical_data.to_csv(f'{OUTPUT_DIR}{ticker['symbol']}_historical_data.csv')
    dividends.to_csv(f'{OUTPUT_DIR}{ticker['symbol']}_dividends.csv')
    info = pd.DataFrame([info])
    info.to_json(f'{OUTPUT_DIR}{ticker['symbol']}_info.json')
