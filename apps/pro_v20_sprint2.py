import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.pro_v20.commander import CommanderCenterV2
from core.pro_v20.tradeplan.trade_planner_v2 import TradePlannerV2
from core.pro_v20.capital.capital_engine_v2 import CapitalEngineV2
from core.pro_v20.risk.risk_engine_v2 import RiskEngineV2
from core.pro_v20.alerts.alert_engine_v2 import AlertEngineV2

st.set_page_config(page_title="LJC Pro V2 Sprint2", page_icon="🧠", layout="wide")
st.title("🧠 LJC Capital AI Pro V2.0 Sprint 2")
st.caption("AI总指挥中心｜Alpha2.0｜资金共振｜风险引擎｜盘中预警｜交易计划")

auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N", 5, 100, 30)

tabs = st.tabs(["AI总指挥", "交易计划", "资金共振", "风险中心", "盘中预警", "手机部署"])

with tabs[0]:
    d = CommanderCenterV2().dashboard()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Alpha2.0", d.get("alpha"))
    c2.metric("风险", d.get("risk"))
    c3.metric("模式", d.get("mode"))
    c4.metric("建议仓位", d.get("position"))
    st.success(d.get("summary"))
    st.subheader("今日Top机会")
    st.dataframe(pd.DataFrame(d.get("top",[])).head(top), use_container_width=True, hide_index=True)

with tabs[1]:
    st.dataframe(TradePlannerV2().plan().head(top), use_container_width=True, hide_index=True)

with tabs[2]:
    st.dataframe(CapitalEngineV2().run().head(top), use_container_width=True, hide_index=True)

with tabs[3]:
    st.dataframe(RiskEngineV2().run().head(top), use_container_width=True, hide_index=True)

with tabs[4]:
    st.dataframe(AlertEngineV2().scan().head(top), use_container_width=True, hide_index=True)

with tabs[5]:
    st.code("python -m streamlit run apps/pro_v20_sprint2_mobile.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
