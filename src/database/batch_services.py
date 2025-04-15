from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, Numeric, MetaData
from database import engine
import pandas as pd

metadata = MetaData()

def create_historic_table(symbol: str):
    table_name = f"{symbol.lower()}_historic_data"

    historic_table = Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True),
        Column("datetime", TIMESTAMP),
        Column("close_price", Numeric(10, 2)),
        Column("volume", Integer),
        extend_existing=True
    )

    try:
        metadata.create_all(engine, tables=[historic_table])
        print(f"Table {table_name} created or already exists.")
    except Exception as e:
        print(f"Failed to create {table_name} due to: {e}")


def create_dividend_table(symbol: str):
    table_name = f"{symbol.lower()}_dividends"

    dividend_table = Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True),
        Column("datetime", TIMESTAMP),
        Column("dividend", Numeric(10, 2)),
        extend_existing=True
    )

    try:
        metadata.create_all(engine, tables=[dividend_table])
        print(f"Table {table_name} created or already exists.")
    except Exception as e:
        print(f"Failed to create {table_name} due to: {e}")


def load_historical_data(symbol: str, df: pd.DataFrame):
    table_name = f"{symbol.lower()}_historic_data"
    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',
            index=False,
            method='multi',
            chunksize=10000
        )
        print(f"Data for {symbol} inserted successfully.")
    except Exception as e:
        print(f"Error inserting data for {symbol}: {e}")

def load_dividend_data(symbol: str, df: pd.DataFrame):
    table_name = f"{symbol.lower()}_dividend"
    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',
            index=False,
            method='multi',
            chunksize=10000
        )
        print(f"DDividend for {symbol} inserted successfully.")
    except Exception as e:
        print(f"Error inserting dividends for {symbol}: {e}")