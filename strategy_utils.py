import pandas as pd

def apply_strategy_filter(df_results, stock_data, fundamentals, config):
    result = []

    for row in df_results.itertuples():
        symbol = row.Symbol
        data = stock_data.get(symbol)
        if data is None or data.empty:
            continue

        today = data.iloc[-1]
        yesterday = data.iloc[-2] if len(data) > 1 else today
        fund = fundamentals.get(symbol, {})

        try:
            if config.get("RSI"):
                rsi = today.get("RSI", None)
                if rsi is None or pd.isna(rsi) or rsi >= 30:
                    continue

            if config.get("SMA"):
                sma5 = today.get("SMA5")
                sma20 = today.get("SMA20")
                if sma5 is None or sma20 is None or pd.isna(sma5) or pd.isna(sma20) or sma5 <= sma20:
                    continue

            if config.get("VOLUME"):
                v_today = today.get("Volume")
                v_yest = yesterday.get("Volume")
                if v_today is None or v_yest is None or pd.isna(v_today) or pd.isna(v_yest) or v_today <= v_yest * 1.5:
                    continue

            if config.get("MACD"):
                macd = today.get("MACD_diff")
                if macd is None or pd.isna(macd) or macd <= 0:
                    continue

            if config.get("CHANGE"):
                c_today = today.get("Close")
                c_yest = yesterday.get("Close")
                if c_today is None or c_yest is None or pd.isna(c_today) or pd.isna(c_yest) or (c_today - c_yest) / c_yest <= 0.03:
                    continue

            if config.get("BREAKOUT"):
                close = today.get("Close")
                if close is None or pd.isna(close):
                    continue
                max20 = data["Close"].rolling(20).max().iloc[-2] if len(data) >= 20 else None
                if max20 is None or pd.isna(max20) or close <= max20:
                    continue

            if config.get("PE")[0] and fund.get("pe", 1000) >= config["PE"][1]:
                continue
            if config.get("PB")[0] and fund.get("pb", 1000) >= config["PB"][1]:
                continue
            if config.get("DE")[0] and fund.get("de", 1000) >= config["DE"][1]:
                continue
            if config.get("EPS")[0] and fund.get("eps_growth", 0) <= config["EPS"][1]:
                continue
            if config.get("DIV")[0] and fund.get("div_yield", 0) <= config["DIV"][1]:
                continue

            result.append({"Symbol": symbol, **fund})
        except:
            continue

    return pd.DataFrame(result)
