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
                rsi = today["RSI"] if "RSI" in today and pd.notna(today["RSI"]) else None
                if rsi is None or rsi >= 30:
                    continue

            if config.get("SMA"):
                sma5 = today["SMA5"] if "SMA5" in today else None
                sma20 = today["SMA20"] if "SMA20" in today else None
                if sma5 is None or sma20 is None or sma5 <= sma20:
                    continue

            if config.get("VOLUME"):
                v_today = today["Volume"] if "Volume" in today else None
                v_yest = yesterday["Volume"] if "Volume" in yesterday else None
                if v_today is None or v_yest is None or v_today <= v_yest * 1.5:
                    continue

            if config.get("MACD"):
                macd = today["MACD_diff"] if "MACD_diff" in today else None
                if macd is None or macd <= 0:
                    continue

            if config.get("CHANGE"):
                c_today = today["Close"] if "Close" in today else None
                c_yest = yesterday["Close"] if "Close" in yesterday else None
                if c_today is None or c_yest is None or (c_today - c_yest) / c_yest <= 0.03:
                    continue

            if config.get("BREAKOUT"):
                close = today["Close"] if "Close" in today else None
                max20 = data["Close"].rolling(20).max().iloc[-2] if "Close" in data and len(data) >= 20 else None
                if close is None or max20 is None or close <= max20:
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
