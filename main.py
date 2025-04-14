import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Config
st.set_page_config(page_title="Dividend & Portfolio Report", layout="wide")

# Tickers and investment
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

# Main Title
st.title("📊 Dividend & Portfolio Dashboard")

# Dropdown at the top
selected_ticker = st.selectbox("Choose an asset", tickers)

# Portfolio return
st.subheader("💼 1-Year Portfolio Performance")
portfolio_value = 0
for ticker in tickers:
    _, price = load_data(ticker)
    start_price = price['Close'][0]
    end_price = price['Close'][-1]
    shares = investment_per_asset / start_price
    final_value = shares * end_price
    portfolio_value += final_value

portfolio_return = ((portfolio_value - total_investment) / total_investment) * 100

col1, col2, col3 = st.columns(3)
col1.metric(label="Initial Investment", value=f"${total_investment}")
col2.metric(label="Portfolio Value (Now)", value=f"${portfolio_value:.2f}")
col3.metric(label="Portfolio Return (1 Year)", value=f"{portfolio_return:.2f}%")

# Dividend Yield Table (above chart)
st.subheader("📈 Dividend Yield (Trailing 12 Months) + Last Dividend Info")
dividend_yield_data = []
for ticker in tickers:
    divs, price = load_data(ticker)
    cutoff_date = pd.Timestamp.today() - pd.DateOffset(years=1)
    divs.index = divs.index.tz_localize(None)
    divs = divs[divs.index >= cutoff_date]

    total_div = divs.sum()
    last_div = divs[-1] if not divs.empty else 0
    last_date = divs.index[-1].strftime('%m/%d/%Y') if not divs.empty else "—"

    try:
        current_price = price['Close'][-1]
        div_yield = total_div / current_price
    except:
        div_yield = 0
    dividend_yield_data.append({
        "Ticker": ticker,
        "Dividend Yield (%)": round(div_yield * 100, 2),
        "Last Dividend Paid ($)": round(last_div, 4),
        "Last Payment Date": last_date
    })

df_yield = pd.DataFrame(dividend_yield_data)
st.dataframe(df_yield.set_index("Ticker"), use_container_width=True)

# Dividend bar chart (last 12 months)
st.subheader(f"📅 Monthly Dividends for {selected_ticker}")
divs, _ = load_data(selected_ticker)
cutoff_date = pd.Timestamp.today() - pd.DateOffset(years=1)
divs.index = divs.index.tz_localize(None)
divs = divs[divs.index >= cutoff_date]
monthly_divs = divs.resample('M').sum()

fig, ax = plt.subplots(figsize=(6, 3))  # Smaller figure
monthly_divs.plot(kind='bar', ax=ax)
ax.set_ylabel("Dividend per Share ($)")
ax.set_xlabel("Month")
ax.set_xticklabels([x.strftime("%m/%Y") for x in monthly_divs.index], rotation=45)
st.pyplot(fig)
