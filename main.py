import streamlit as st
import json
from strategy_utils import apply_strategy_filter
from model_utils import load_data, load_fundamentals, get_sp500_symbols
from chart_utils import show_stock_chart

st.set_page_config(page_title="📈 AI 自動選股平台 - S&P 500", layout="wide")
st.title("📈 AI 選股平台（S&P 500 全自動分析）")

st.markdown("🔍 本平台將自動分析 S&P 500 所有股票，根據技術與基本面條件篩選。")

st.header("📋 自訂選股條件")

use_rsi = st.checkbox("RSI < 30", value=True)
use_sma = st.checkbox("SMA5 > SMA20", value=True)
use_volume = st.checkbox("成交量 > 昨日 1.5倍", value=True)
use_macd = st.checkbox("MACD 黃金交叉", value=True)
use_change = st.checkbox("今日漲幅 > 3%", value=True)
use_breakout = st.checkbox("突破20日新高", value=True)

st.header("📘 財報條件")
use_pe = st.checkbox("P/E Ratio < 15", value=True)
use_pb = st.checkbox("P/B Ratio < 2", value=True)
use_de = st.checkbox("D/E Ratio < 1", value=True)
use_eps = st.checkbox("EPS YoY 增長 > 10%", value=True)
use_div = st.checkbox("Dividend Yield > 3%", value=True)

if st.button("🚀 開始分析 S&P 500"):
    config = {
        "RSI": use_rsi, "SMA": use_sma, "VOLUME": use_volume,
        "MACD": use_macd, "CHANGE": use_change, "BREAKOUT": use_breakout,
        "PE": [use_pe, 15], "PB": [use_pb, 2], "DE": [use_de, 1.0],
        "EPS": [use_eps, 10], "DIV": [use_div, 3]
    }

    symbols = get_sp500_symbols()
    df_results, stock_data = load_data(symbols)
    df_fundamentals = load_fundamentals(symbols)
    df_filtered = apply_strategy_filter(df_results, stock_data, df_fundamentals, config)

    st.subheader("✅ 符合條件的股票")
    st.dataframe(df_filtered)

    for sym in df_filtered["Symbol"].head(5):  # 限制顯示前5圖表
        st.plotly_chart(show_stock_chart(stock_data[sym], sym))
