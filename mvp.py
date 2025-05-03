# Free Tier Backtest Code Generator (Streamlit)

import streamlit as st
from datetime import date
import yfinance as yf
import pandas as pd
import vectorbt as vbt

# ---------------------- UI Layout ---------------------- #
st.title("🔁 Free Backtest Code Generator")

with st.form("strategy_form"):
    symbol = st.text_input("📈 股票代碼 (e.g. AAPL)", value="AAPL")
    start_date = st.date_input("開始日期", value=date(2022, 1, 1))
    end_date = st.date_input("結束日期", value=date.today())
    fast_ma = st.number_input("快速均線期數", value=5)
    slow_ma = st.number_input("慢速均線期數", value=20)
    tp = st.number_input("Take Profit (%)", value=10.0)
    sl = st.number_input("Stop Loss (%)", value=5.0)
    submitted = st.form_submit_button("產生回測")

if submitted:
    st.subheader("🚀 自動產生的回測結果")

    # 下載資料
    data = yf.download(symbol, start=start_date, end=end_date)
    price = data['Close']

    # 策略邏輯：均線交叉
    fast = vbt.MA.run(price, window=fast_ma)
    slow = vbt.MA.run(price, window=slow_ma)
    entries = fast.ma_crossed_above(slow)
    exits = fast.ma_crossed_below(slow)

    # 設定回測
    pf = vbt.Portfolio.from_signals(
        close=price,
        entries=entries,
        exits=exits,
        stop_loss=sl / 100,
        take_profit=tp / 100,
        direction="longonly",
        fees=0.001,
        slippage=0.001
    )

    # 顯示結果
    st.plotly_chart(pf.plot())
    st.dataframe(pf.stats().to_frame())

    # 產出程式碼
    code = f"""
import yfinance as yf
import vectorbt as vbt

symbol = '{symbol}'
data = yf.download(symbol, start='{start_date}', end='{end_date}')
price = data['Close']

fast = vbt.MA.run(price, window={fast_ma})
slow = vbt.MA.run(price, window={slow_ma})

entries = fast.ma_crossed_above(slow)
exits = fast.ma_crossed_below(slow)

pf = vbt.Portfolio.from_signals(
    close=price,
    entries=entries,
    exits=exits,
    stop_loss={sl} / 100,
    take_profit={tp} / 100,
    direction='longonly',
    fees=0.001,
    slippage=0.001
)

pf.plot().show()
print(pf.stats())
"""

    st.subheader("📄 Python 程式碼")
    st.code(code, language="python")
