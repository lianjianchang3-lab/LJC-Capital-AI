import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from core.cockpit import TradingCockpit

st.set_page_config(page_title="LJC V8.5 Cockpit Mobile", page_icon="📱", layout="centered")
snap = TradingCockpit().snapshot()
market = snap.get("market", {}) or {}

st.title("📱 LJC V8.5 驾驶舱")
c1,c2 = st.columns(2)
c1.metric("市场", market.get("state","-"))
c2.metric("仓位", market.get("position","-"))
st.success(snap.get("summary","-"))

st.subheader("今天可以买")
buy = snap.get("buy")
if buy is None or buy.empty:
    st.info("暂无")
else:
    for _, r in buy.head(8).iterrows():
        st.success(f"{r.get('code')} {r.get('name')}｜优先级{r.get('买入优先级')}｜首仓{r.get('首次建仓')}｜最大{r.get('最大允许仓位')}")
        st.caption(f"买点 {r.get('第一买点')}/{r.get('第二买点')}｜止损 {r.get('止损价')}｜目标 {r.get('第一止盈')}/{r.get('第二止盈')}")

st.subheader("风险/减仓")
items = []
reduce = snap.get("reduce")
avoid = snap.get("avoid")
if reduce is not None and not reduce.empty:
    items += reduce.to_dict("records")
if avoid is not None and not avoid.empty:
    items += avoid.to_dict("records")
if not items:
    st.info("暂无明显风险")
for r in items[:8]:
    st.error(f"{r.get('code')} {r.get('name')}｜{r.get('持仓建议') or r.get('V8动作')}｜{r.get('执行结论') or r.get('组合操作')}")
