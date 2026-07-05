import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from core.trader import AITrader

st.set_page_config(page_title="LJC V5.1 Mobile", page_icon="📱", layout="centered")
st.title("📱 LJC V5.1 AI Trader")

df = AITrader().signals()
if df.empty:
    st.warning("暂无信号")
else:
    c1,c2 = st.columns(2)
    c1.metric("最高强度", df["AI交易强度"].max())
    c2.metric("买入关注", int((df["执行建议"]=="买入关注").sum()))
    st.subheader("今日执行")
    for _, r in df.head(8).iterrows():
        line = f"{r.get('执行建议')}｜{r.get('code')} {r.get('name')}｜强度{r.get('AI交易强度')}｜仓位{r.get('建议仓位V5')}"
        if r.get("执行建议") == "买入关注":
            st.success(line)
        elif "回避" in str(r.get("执行建议")):
            st.error(line)
        else:
            st.info(line)
        st.caption(f"买点 {r.get('第一买点')}/{r.get('第二买点')}｜止损 {r.get('止损价')}｜目标 {r.get('第一止盈')}/{r.get('第二止盈')}")
