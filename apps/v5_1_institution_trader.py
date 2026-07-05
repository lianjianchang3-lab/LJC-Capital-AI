import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.institution import InstitutionEngine
from core.trader import AITrader
from core.decision import DecisionCore

st.set_page_config(page_title="LJC V5.1 Institution Trader", page_icon="🏛️", layout="wide")
st.title("🏛️ LJC Capital AI Pro V5.1")
st.caption("Institution Engine｜AI Trader｜机构共振｜买卖点｜执行计划")

auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N", 5, 100, 30)

tabs = st.tabs(["AI Trader", "机构引擎", "DecisionCore", "今日执行计划", "手机部署"])

with tabs[0]:
    df = AITrader().signals()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("信号数", len(df))
    c2.metric("最高交易强度", df["AI交易强度"].max() if not df.empty else "-")
    c3.metric("买入关注", int((df["执行建议"]=="买入关注").sum()) if not df.empty else 0)
    c4.metric("小仓试探", int((df["执行建议"]=="小仓试探").sum()) if not df.empty else 0)
    st.dataframe(df.head(top), use_container_width=True, hide_index=True)

with tabs[1]:
    st.dataframe(InstitutionEngine().run().head(top), use_container_width=True, hide_index=True)

with tabs[2]:
    dc = DecisionCore()
    st.json(dc.market())
    st.dataframe(dc.trade_plan().head(top), use_container_width=True, hide_index=True)

with tabs[3]:
    st.text(AITrader().today_plan_text())

with tabs[4]:
    st.code("python -m streamlit run apps/v5_1_mobile.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
