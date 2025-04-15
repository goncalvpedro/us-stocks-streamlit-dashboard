import pandas as pd
from api import yf_api
from database.db import Portfolio

initial_data = [
    {'symbol': 'SGOV', 'shares': 4.565, 'price': 100.49, 'first_acquisition': '2024-10-03'},
    {'symbol': 'STAG', 'shares': 6.211, 'price': 34.62, 'first_acquisition': '2024-10-02'},
    {'symbol': 'SPG', 'shares': 1.344, 'price': 160.00, 'first_acquisition': '2024-10-08'},
    {'symbol': 'O', 'shares': 2.960, 'price': 57.10, 'first_acquisition': '2024-10-03'},
    {'symbol': 'SPY', 'shares': 0.334, 'price': 547.46, 'first_acquisition': '2024-10-03'},
    {'symbol': 'INDA', 'shares': 2.018, 'price': 51.15, 'first_acquisition': '2024-10-03'},
    {'symbol': 'FXI', 'shares': 3.796, 'price': 30.38, 'first_acquisition': '2024-10-03'},
]

def load_initial_data(data):
    for item in data:
        if not all([item.get('symbol'), item.get('shares'), item.get('price'), item.get('first_acquisition')]):
            print('Missing information in item:', item)
            continue
        
        date = pd.to_datetime(item['first_acquisition']).date()
        
        Portfolio.create_item(
            item['symbol'],
            item['shares'],
            item['price'],
            date
        )

load_initial_data(initial_data)
