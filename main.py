import streamlit as st
from model_utils import load_data_and_predict

st.set_page_config(page_title="AI 選股平台", layout="wide")

st.title("📈 AI 智能美股選股平台")
st.markdown("使用預設AI模型分析全美股數據，找出潛力股票。")

selected_symbols = st.text_input("輸入股票代碼（用逗號分隔，例如：AAPL, MSFT, TSLA）", "AAPL, MSFT, TSLA")
symbols = [s.strip().upper() for s in selected_symbols.split(",")]

if st.button("開始分析"):
    with st.spinner("正在分析中..."):
        df_results = load_data_and_predict(symbols)
        st.success("分析完成！")
        st.dataframe(df_results)

        csv = df_results.to_csv(index=False).encode("utf-8")
        st.download_button("📥 下載分析結果 (CSV)", csv, "results.csv", "text/csv")

st.markdown("---")
st.markdown("💡 本平台由AI模型驅動，結合移動平均與RSI等技術指標，協助你挖掘潛力股。")
