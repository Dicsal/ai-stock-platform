import streamlit as st
from model_utils import load_data_and_predict
from chart_utils import show_stock_chart
from ai_score_utils import score_stocks

st.set_page_config(page_title="AI 選股平台", layout="wide")

st.title("📈 AI 智能美股選股平台")
st.markdown("使用 AI 模型分析全美股數據，並顯示走勢圖與選股排名。")

selected_symbols = st.text_input("輸入股票代碼（用逗號分隔，例如：AAPL, MSFT, TSLA）", "AAPL, MSFT, TSLA")
symbols = [s.strip().upper() for s in selected_symbols.split(",")]

if st.button("開始分析"):
    with st.spinner("正在分析與建圖中..."):
        df_results, stock_data = load_data_and_predict(symbols)
        df_scored = score_stocks(df_results)

        st.success("分析完成 ✅")
        st.subheader("📊 AI 選股打分排行榜")
        st.dataframe(df_scored)

        csv = df_scored.to_csv(index=False).encode("utf-8")
        st.download_button("📥 下載分析結果 (CSV)", csv, "ai_score_results.csv", "text/csv")

        st.subheader("📈 K線走勢圖 + 技術指標")
        for symbol in symbols:
            if symbol in stock_data:
                st.plotly_chart(show_stock_chart(stock_data[symbol], symbol))
