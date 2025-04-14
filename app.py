import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Config
st.set_page_config(page_title="Dividend & Portfolio Report", layout="wide")

# Tickers and initial investment
tickers = ['SGOV', 'STAG', 'SPG', 'O', 'INDA', 'FXI', 'SPY']
investment_per_asset = 100
total_investment = investment_per_asset * len(tickers)

# Load data
@st.cache_data
def load_data(ticker):
    stock = yf.Ticker(ticker)
    divs = stock.dividends
    price = stock.history(period='1y')
    return divs, price

# Sidebar - dropdown
selected_ticker = st.sidebar.selectbox("Choose an asset", tickers)

# Dividend bar chart (last 12 months)
divs, _ = load_data(selected_ticker)
divs = divs[divs.index >= (pd.Timestamp.today() - pd.DateOffset(years=1))]
monthly_divs = divs.resample('M').sum()

st.title("Dividend & Portfolio Dashboard")

st.subheader(f"Dividend Payments for {selected_ticker}")
fig, ax = plt.subplots()
monthly_divs.plot(kind='bar', ax=ax)
ax.set_ylabel("Dividend per Share ($)")
ax.set_xlabel("Month")
st.pyplot(fig)

# Dividend Yield for all tickers
st.subheader("Dividend Yield (Trailing 12 Months)")
dividend_yield_data = []
for ticker in tickers:
    divs, price = load_data(ticker)
    divs = divs[divs.index >= (pd.Timestamp.today() - pd.DateOffset(years=1))]
    total_div = divs.sum()
    try:
        current_price = price['Close'][-1]
        div_yield = total_div / current_price
    except:
        div_yield = 0
    dividend_yield_data.append({
        "Ticker": ticker,
        "Dividend Yield (%)": round(div_yield * 100, 2)
    })

df_yield = pd.DataFrame(dividend_yield_data)
st.dataframe(df_yield.set_index("Ticker"))

# Portfolio return
st.subheader("1-Year Portfolio Return")

portfolio_value = 0
for ticker in tickers:
    _, price = load_data(ticker)
    start_price = price['Close'][0]
    end_price = price['Close'][-1]
    shares = investment_per_asset / start_price
    final_value = shares * end_price
    portfolio_value += final_value

portfolio_return = ((portfolio_value - total_investment) / total_investment) * 100

st.metric(label="Initial Investment", value=f"${total_investment}")
st.metric(label="Portfolio Value (Now)", value=f"${portfolio_value:.2f}")
st.metric(label="Portfolio Return (1 Year)", value=f"{portfolio_return:.2f}%")
