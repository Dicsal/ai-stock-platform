import yfinance as yf
import pandas as pd
import requests
import random

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def compute_macd(close):
    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    macd_line = ema12 - ema26
    signal = macd_line.ewm(span=9).mean()
    return macd_line - signal

def get_sp500_symbols():
    url = "https://datahub.io/core/s-and-p-500-companies/r/constituents.csv"
    df = pd.read_csv(url)
    return df["Symbol"].tolist()

def load_data(symbols):
    results = []
    stock_data = {}

    for sym in symbols:
        try:
            data = yf.download(sym, start="2023-01-01", end="2024-12-31")
            if data.empty:
                continue
            data['SMA5'] = data['Close'].rolling(5).mean()
            data['SMA20'] = data['Close'].rolling(20).mean()
            data['RSI'] = compute_rsi(data['Close'])
            data['MACD_diff'] = compute_macd(data['Close'])
            data.dropna(inplace=True)
            stock_data[sym] = data.copy()
            results.append({"Symbol": sym})
        except Exception:
            continue

    return pd.DataFrame(results), stock_data

def load_fundamentals(symbols):
    fundamentals = {}
    for sym in symbols:
        fundamentals[sym] = {
            "pe": random.uniform(5, 30),
            "pb": random.uniform(0.5, 5),
            "de": random.uniform(0, 3),
            "eps_growth": random.uniform(-10, 50),
            "div_yield": random.uniform(0, 6),
        }
    return fundamentals
