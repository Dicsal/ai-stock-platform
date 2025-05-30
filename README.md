# AI 選股平台部署指南

這是一個基於 Streamlit 的 AI 股票選股平台，可分析多支美股並輸出預測準確率。

## 🚀 快速啟動

```bash
pip install -r requirements.txt
streamlit run main.py
```

## ☁️ 部署到 Streamlit Cloud

1. 建立 GitHub 倉庫並上傳所有檔案
2. 前往 https://streamlit.io/cloud 並登入
3. 點選「New App」，選擇你剛上傳的 GitHub 專案
4. 輸入 `main.py` 為啟動腳本，點擊「Deploy」
5. 完成！

## 📌 注意事項
- 使用 yfinance 為免費資料源，可能有速率限制
- 每次輸入建議控制在 3-5 支股票內
