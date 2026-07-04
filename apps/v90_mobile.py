import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.v90 import V90RealtimeManager, V90DecisionEngine

st.set_page_config(page_title="LJC V9.0 Mobile", page_icon="📱", layout="centered")

st.title("📱 LJC V9.0 Mobile")
st.caption("实时数据｜AI决策｜交易计划")

data = V90RealtimeManager()
engine = V90DecisionEngine()
health = data.health()
plan = engine.trading_plan()

st.subheader("今日状态")
c1, c2 = st.columns(2)
c1.metric("数据源", health.get("active_source"))
c2.metric("行数", health.get("active_rows"))

st.subheader("AI结论")
st.success(engine.dashboard().get("committee_summary"))
st.info(plan.get("risk_note"))

st.subheader("交易计划")
actions = plan.get("actions", [])
if actions:
    st.dataframe(pd.DataFrame(actions), use_container_width=True, hide_index=True)
else:
    st.warning("暂无交易计划。")
