import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from core.decision import DecisionCore

st.set_page_config(page_title="LJC V5 Mobile", page_icon="📱", layout="centered")
st.title("📱 LJC V5 Decision Core")
dc = DecisionCore()
m = dc.market()
c1,c2 = st.columns(2)
c1.metric("市场", m.get("state"))
c2.metric("仓位", m.get("position"))
st.success(m.get("summary"))

plan = dc.trade_plan()
st.subheader("今日重点")
for _, r in plan.head(8).iterrows():
    line = f"{r.get('Action')}｜{r.get('code')} {r.get('name')}｜LCRI {r.get('LCRI Score')}｜仓位 {r.get('Position')}"
    if r.get("Action") == "A类关注":
        st.success(line)
    elif r.get("Action") == "C类回避":
        st.error(line)
    else:
        st.info(line)
    st.caption(f"买入区：{r.get('Buy Zone')}｜止损：{r.get('Stop Loss')}｜目标：{r.get('Target 1')}/{r.get('Target 2')}")
