import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.decision import DecisionCore
from core.data import MarketDataService

st.set_page_config(page_title="LJC V5 DataOS DecisionCore", page_icon="🧠", layout="wide")
st.title("🧠 LJC Capital AI Pro V5.0 Alpha")
st.caption("Data OS｜Factor Engine｜Decision Core｜统一决策入口")

dc = DecisionCore()
auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N", 5, 100, 30)

tabs = st.tabs(["Decision Core", "Data OS", "Factor Scores", "Trade Plan", "Portfolio", "Morning Report", "手机部署"])

with tabs[0]:
    m = dc.market()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("市场状态", m.get("state"))
    c2.metric("LCRI均分", m.get("lcri_avg"))
    c3.metric("建议仓位", m.get("position"))
    c4.metric("A类数量", m.get("buy_count"))
    st.success(m.get("summary"))

with tabs[1]:
    st.json(MarketDataService().health())
    st.dataframe(MarketDataService().dataframe().head(top), use_container_width=True, hide_index=True)

with tabs[2]:
    st.dataframe(dc.stocks().head(top), use_container_width=True, hide_index=True)

with tabs[3]:
    st.dataframe(dc.trade_plan().head(top), use_container_width=True, hide_index=True)

with tabs[4]:
    p = dc.portfolio()
    st.success(p.get("summary"))
    st.dataframe(pd.DataFrame(p.get("holdings",[])), use_container_width=True, hide_index=True)

with tabs[5]:
    st.text(dc.morning_report())

with tabs[6]:
    st.code("python -m streamlit run apps/v5_mobile.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
