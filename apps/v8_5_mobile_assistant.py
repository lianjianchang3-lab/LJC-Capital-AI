import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

import streamlit as st
from core.enterprise import EnterpriseCommander
from core.execution import ExecutionCenter

st.set_page_config(page_title="LJC V8.5 Mobile", page_icon="📱", layout="centered")
snap = EnterpriseCommander().snapshot()
market = snap.get("market", {}) or {}
df = ExecutionCenter().dataframe()

st.title("📱 LJC V8.5")
c1,c2 = st.columns(2)
c1.metric("市场", market.get("state","-"))
c2.metric("仓位", market.get("position","-"))
st.success(snap.get("summary","-"))
st.subheader("今日交易助手")
for _, r in df.head(10).iterrows():
    text = f"优先级{r.get('买入优先级')}｜{r.get('code')} {r.get('name')}｜{r.get('V8动作')}｜首仓{r.get('首次建仓')}｜最大{r.get('最大允许仓位')}"
    if r.get("买入优先级") in [1,2]:
        st.success(text)
    elif r.get("买入优先级") == 9:
        st.error(text)
    else:
        st.info(text)
    st.caption(f"买点 {r.get('第一买点')}/{r.get('第二买点')}｜止损 {r.get('止损价')}｜目标 {r.get('第一止盈')}/{r.get('第二止盈')}")
