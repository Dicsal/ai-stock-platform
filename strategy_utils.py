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

        pass_filter = True

        if config.get("RSI") and pd.notna(today.get("RSI")) and today["RSI"] >= 30:
            pass_filter = False
        if config.get("SMA") and pd.notna(today.get("SMA5")) and pd.notna(today.get("SMA20")) and today["SMA5"] <= today["SMA20"]:
            pass_filter = False
        if config.get("VOLUME") and pd.notna(today.get("Volume")) and pd.notna(yesterday.get("Volume")) and today["Volume"] <= yesterday["Volume"] * 1.5:
            pass_filter = False
        if config.get("MACD") and pd.notna(today.get("MACD_diff")) and today["MACD_diff"] <= 0:
            pass_filter = False
        if config.get("CHANGE") and pd.notna(today.get("Close")) and pd.notna(yesterday.get("Close")) and (today["Close"] - yesterday["Close"]) / yesterday["Close"] <= 0.03:
            pass_filter = False
        if config.get("BREAKOUT") and pd.notna(today.get("Close")) and pd.notna(data["Close"].rolling(20).max().iloc[-2]):
            if today["Close"] <= data["Close"].rolling(20).max().iloc[-2]:
                pass_filter = False

        if config.get("PE")[0] and fund.get("pe", 1000) >= config["PE"][1]:
            pass_filter = False
        if config.get("PB")[0] and fund.get("pb", 1000) >= config["PB"][1]:
            pass_filter = False
        if config.get("DE")[0] and fund.get("de", 1000) >= config["DE"][1]:
            pass_filter = False
        if config.get("EPS")[0] and fund.get("eps_growth", 0) <= config["EPS"][1]:
            pass_filter = False
        if config.get("DIV")[0] and fund.get("div_yield", 0) <= config["DIV"][1]:
            pass_filter = False

        if pass_filter:
            result.append({"Symbol": symbol, **fund})

    return pd.DataFrame(result)
