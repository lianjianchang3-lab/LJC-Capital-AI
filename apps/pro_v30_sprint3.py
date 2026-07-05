import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.pro_v30 import PortfolioCenterV3, MorningBriefPro, TradeLogbook
from core.pro_v20.commander import CommanderCenterV2
from core.pro_v20.tradeplan.trade_planner_v2 import TradePlannerV2

st.set_page_config(page_title="LJC Pro V3 Sprint3", page_icon="🏦", layout="wide")
st.title("🏦 LJC Pro V3.0 Sprint 3 股票管理中心")
st.caption("持仓作战｜晨会Pro｜AI交易日志｜今日总指挥")

auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)

tabs = st.tabs(["总指挥", "股票管理中心", "晨会Pro", "AI交易日志", "交易计划", "手机部署"])

with tabs[0]:
    d = CommanderCenterV2().dashboard()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Alpha", d.get("alpha"))
    c2.metric("风险", d.get("risk"))
    c3.metric("模式", d.get("mode"))
    c4.metric("仓位", d.get("position"))
    st.success(d.get("summary"))
    st.dataframe(pd.DataFrame(d.get("top",[])), use_container_width=True, hide_index=True)

with tabs[1]:
    p = PortfolioCenterV3().analyze()
    st.success(p.get("summary"))
    st.json(p.get("total"))
    st.dataframe(p.get("table"), use_container_width=True, hide_index=True)
    st.info("编辑 data/portfolio/holdings.csv 填入 cost 和 shares，即可计算真实盈亏。")

with tabs[2]:
    m = MorningBriefPro()
    st.text(m.text())

with tabs[3]:
    log = TradeLogbook()
    if st.button("记录一次AI建议快照"):
        n = log.add_ai_snapshot()
        st.success(f"已记录 {n} 条AI建议")
    st.dataframe(log.read(), use_container_width=True, hide_index=True)

with tabs[4]:
    st.dataframe(TradePlannerV2().plan(), use_container_width=True, hide_index=True)

with tabs[5]:
    st.code("python -m streamlit run apps/pro_v30_mobile.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
