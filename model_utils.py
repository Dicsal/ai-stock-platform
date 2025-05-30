import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def load_data_and_predict(symbols):
    results = []
    stock_data = {}

    for symbol in symbols:
        try:
            data = yf.download(symbol, start="2021-01-01", end="2024-12-31")
            data['SMA5'] = data['Close'].rolling(5).mean()
            data['SMA20'] = data['Close'].rolling(20).mean()
            data['RSI'] = compute_rsi(data['Close'])
            data.dropna(inplace=True)
            data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int)

            X = data[['SMA5', 'SMA20', 'RSI']]
            y = data['Target']

            model = RandomForestClassifier(n_estimators=100)
            model.fit(X[:-50], y[:-50])
            pred = model.predict(X[-50:])
            acc = (pred == y[-50:]).mean()

            results.append({'股票代碼': symbol, '預測準確率': round(acc * 100, 2), '最新RSI': round(data['RSI'].iloc[-1], 2)})
            stock_data[symbol] = data.copy()
        except Exception as e:
            results.append({'股票代碼': symbol, '預測準確率': 0, '最新RSI': 0})

    return pd.DataFrame(results), stock_data
