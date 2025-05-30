import pandas as pd

def score_stocks(df):
    df['AI綜合分數'] = df['預測準確率'] * 0.7 + (100 - abs(df['最新RSI'] - 50)) * 0.3
    return df.sort_values(by='AI綜合分數', ascending=False)
