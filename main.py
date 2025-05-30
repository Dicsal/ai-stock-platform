import streamlit as st
import json
from strategy_utils import apply_strategy_filter
from model_utils import load_data, load_fundamentals
from chart_utils import show_stock_chart

st.set_page_config(page_title="AI 選股策略平台（技術 + 財報）", layout="wide")
st.title("📊 自定義選股策略平台")

symbols_input = st.text_input("輸入股票代碼（如：AAPL, TSLA, MSFT）", "AAPL, TSLA")
symbols = [s.strip().upper() for s in symbols_input.split(",")]

st.header("📋 技術條件")
use_rsi = st.checkbox("RSI < 30")
use_sma = st.checkbox("SMA5 > SMA20")
use_volume = st.checkbox("成交量 > 昨日1.5倍")
use_macd = st.checkbox("MACD 黃金交叉")
use_change = st.checkbox("今日漲幅 > 3%")
use_breakout = st.checkbox("突破20日新高")

st.header("📘 財報條件")
use_pe = st.checkbox("P/E Ratio <")
pe_val = st.number_input("P/E 值上限", value=15.0)
use_pb = st.checkbox("P/B Ratio <")
pb_val = st.number_input("P/B 值上限", value=2.0)
use_de = st.checkbox("Debt-to-Equity <")
de_val = st.number_input("D/E 上限", value=1.0)
use_eps = st.checkbox("EPS YoY 增長 >")
eps_val = st.number_input("EPS 增長率 (%)", value=10.0)
use_div = st.checkbox("Dividend Yield >")
div_val = st.number_input("股息殖利率 (%)", value=3.0)

if st.button("儲存策略"):
    config = {
        "RSI": use_rsi, "SMA": use_sma, "VOLUME": use_volume,
        "MACD": use_macd, "CHANGE": use_change, "BREAKOUT": use_breakout,
        "PE": [use_pe, pe_val], "PB": [use_pb, pb_val],
        "DE": [use_de, de_val], "EPS": [use_eps, eps_val],
        "DIV": [use_div, div_val]
    }
    with open("strategy_config.json", "w") as f:
        json.dump(config, f)
    st.success("策略設定已儲存 ✅")

if st.button("執行分析"):
    try:
        with open("strategy_config.json") as f:
            config = json.load(f)
    except:
        st.error("請先儲存策略")
        st.stop()

    df_results, stock_data = load_data(symbols)
    df_fundamentals = load_fundamentals(symbols)
    df_filtered = apply_strategy_filter(df_results, stock_data, df_fundamentals, config)

    st.subheader("✅ 符合條件股票清單")
    st.dataframe(df_filtered)

    for sym in df_filtered["Symbol"]:
        st.plotly_chart(show_stock_chart(stock_data[sym], sym))
