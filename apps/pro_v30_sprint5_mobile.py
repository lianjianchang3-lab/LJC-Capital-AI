import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.pro_v30.commander import CommanderProV5
from core.pro_v30.calendar import TradeCalendarV5

st.set_page_config(page_title="LJC Commander Pro", page_icon="📱", layout="centered")
st.title("📱 LJC Commander Pro")
d = CommanderProV5().dashboard()
c1,c2 = st.columns(2)
c1.metric("模式", d.get("mode"))
c2.metric("风险", d.get("risk_level"))
st.success(d.get("risk_summary"))
st.caption(f"组合Alpha：{d.get('portfolio_alpha')}｜回撤预估：{d.get('drawdown_est')}｜Sharpe：{d.get('sharpe_est')}")

st.subheader("今日信号")
for x in d.get("top", [])[:8]:
    line = f"{x.get('信号')}｜{x.get('code')} {x.get('name')}｜强度{x.get('信号强度')}｜仓位{x.get('建议仓位')}"
    if x.get("信号") == "买入":
        st.success(line)
    elif "回避" in str(x.get("信号")):
        st.error(line)
    else:
        st.info(line)
    st.caption(x.get("一句话建议"))

with st.expander("AI交易日历"):
    st.text(TradeCalendarV5().text())
