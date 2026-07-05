import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.pro_v30.commander import CommanderProV5
from core.pro_v30.signal import SignalCenterV5
from core.pro_v30.risk import PortfolioRiskV5
from core.pro_v30.calendar import TradeCalendarV5

st.set_page_config(page_title="LJC Pro V3 Sprint5", page_icon="🛰️", layout="wide")
st.title("🛰️ LJC Pro V3.0 Sprint 5 机构级决策引擎")
st.caption("买卖信号中心｜组合风险｜AI交易日历｜Commander Pro")

auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
topn = st.sidebar.slider("显示前N", 5, 100, 30)

tabs = st.tabs(["Commander Pro", "买卖信号", "组合风险", "AI交易日历", "手机部署"])

with tabs[0]:
    d = CommanderProV5().dashboard()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("模式", d.get("mode"))
    c2.metric("风险等级", d.get("risk_level"))
    c3.metric("组合Alpha", d.get("portfolio_alpha"))
    c4.metric("回撤预估", d.get("drawdown_est"))
    st.success(d.get("risk_summary"))
    st.subheader("今日最强信号")
    st.dataframe(pd.DataFrame(d.get("top",[])).head(topn), use_container_width=True, hide_index=True)

with tabs[1]:
    st.dataframe(SignalCenterV5().signals().head(topn), use_container_width=True, hide_index=True)

with tabs[2]:
    r = PortfolioRiskV5().analyze()
    st.success(r.get("summary"))
    st.json({k:v for k,v in r.items() if k not in ["table"]})
    st.dataframe(r.get("table"), use_container_width=True, hide_index=True)

with tabs[3]:
    st.text(TradeCalendarV5().text())

with tabs[4]:
    st.code("python -m streamlit run apps/pro_v30_sprint5_mobile.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
