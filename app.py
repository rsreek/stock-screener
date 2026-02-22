import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Indian Stock Screener", layout="wide")
st.title("📈 Indian Stock Screener - Midcap & Largecap")

# --- Stock Lists ---
LARGECAP = {
    "Reliance Industries": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "SBI": "SBIN.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "ITC": "ITC.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
}

MIDCAP = {
    "Persistent Systems": "PERSISTENT.NS",
    "Tube Investments": "TIINDIA.NS",
    "Coforge": "COFORGE.NS",
    "Voltas": "VOLTAS.NS",
    "MRF": "MRF.NS",
    "Godrej Properties": "GODREJPROP.NS",
    "Trent": "TRENT.NS",
    "Astral": "ASTRAL.NS",
    "PI Industries": "PIIND.NS",
    "Mphasis": "MPHASIS.NS",
    "Lodha": "LODHA.NS",
}

# --- Sidebar Filters ---
st.sidebar.header("Filters")
cap_type = st.sidebar.radio("Select Category", ["Largecap", "Midcap"])
period = st.sidebar.selectbox("Period", ["1mo", "3mo", "6mo", "1y"])

stock_list = LARGECAP if cap_type == "Largecap" else MIDCAP
selected_name = st.sidebar.selectbox("Select Stock", list(stock_list.keys()))
selected_ticker = stock_list[selected_name]

# --- Fetch Data ---
st.subheader(f"{selected_name} ({selected_ticker})")
df = yf.download(selected_ticker, period=period)

if not df.empty:
    # Candlestick Chart
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )])
    fig.update_layout(title=f"{selected_name} Price Chart", xaxis_title="Date", yaxis_title="Price (INR)")
    st.plotly_chart(fig, width='stretch')

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"₹{float(df['Close'].iloc[-1]):.2f}")
    col2.metric("52W High", f"₹{float(df['High'].max()):.2f}")
    col3.metric("52W Low", f"₹{float(df['Low'].min()):.2f}")

    # Raw data
    st.subheader("Recent Data")
    st.dataframe(df.tail(10))
else:
    st.error("No data found!")
