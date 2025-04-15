import yfinance as yf
from datetime import datetime as dt


def load_ticker_data(ticker):
    if not isinstance(ticker, str):
        return print(f'Attribute must be a list. Type received was {type(ticker)}')

    try:
        stock = yf.Ticker(ticker)
        return stock
    except Exception as e:
        return print(f'Unable to load data ({ticker}) due an error: {e}')


def load_tickers_data(tickers_list):
    if not isinstance(tickers_list, list):
        return print(f'Attribute must be a list. Type received was {type(tickers_list)}')

    try:
        stocks = yf.Tickers(tickers_list)
        return stocks
    except Exception as e:
        return print(f'Unable to load data due an error: {e}')

today = dt.today().strftime('%Y-%m-%d')

def get_historical_data(ticker, start_date, end_date=today):
    if not isinstance(ticker, str):
        return print(f'Attribute must be a list. Type received was {type(ticker)}')

    try:

        ticker_history = yf.download([ticker], start=start_date, end=end_date)
        return ticker_history
    
    except Exception as e:
        return print(f'Unable to fetch historical data from {ticker} due an error: {e}')


def get_dividends(ticker):
    if not isinstance(ticker, str):
        return print(f'Attribute must be a str. Type received was {type(ticker)}')

    try:
        ticker_object = load_ticker_data(ticker)
        dividends = ticker_object.dividends
        return dividends

    except Exception as e:
        return print(f'Unable to fetch dividends from {ticker} due an error: {e}')

def get_ticker_info(ticker):
    if not isinstance(ticker, str):
        return print(f'Attribute must be a str. Type received was {type(ticker)}')

    try:
        ticker_object = load_ticker_data(ticker)
        ticker_info = ticker_object.info
        return ticker_info

    except Exception as e:
        return print(f'Unable to fetch information for {ticker} due an error: {e}')

