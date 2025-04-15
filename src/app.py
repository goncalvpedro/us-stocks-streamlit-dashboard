import pandas as pd
from api import yf_api
from database.db import Portfolio
from database import batch_services


portfolio = Portfolio()

portfolio = portfolio.read_portfolio()

def to_dict(obj):
    return {col.name: getattr(obj, col.name) for col in obj.__table__.columns}

portfolio_dicts = [to_dict(p) for p in portfolio]

df = pd.DataFrame(portfolio_dicts)

for row in df.iterrows():
    row = row[1]
    symbol = row['symbol']
    first_acquisition = row['first_acquisition']

    historical_data = yf_api.get_historical_data(symbol, first_acquisition)
    dividends = yf_api.get_dividends(symbol)
    info = yf_api.get_ticker_info(symbol)

    historical_data = historical_data.loc[:, [('Close', symbol), ('Volume', symbol)]].droplevel('Ticker', axis=1).reset_index().rename(columns={'Date':'datetime','Close': 'close_price', 'Volume':'volume'})
    dividends = pd.DataFrame(dividends)

    dividends = dividends.reset_index().rename(columns={'Date': 'datetime','Dividends': 'dividend'})

    if isinstance(dividends, pd.DataFrame):
        batch_services.load_historical_data(symbol, historical_data)
        batch_services.load_dividend_data(symbol, dividends)
    
    else:
        print(f'historical data type: {type(dividends)}')
        continue
