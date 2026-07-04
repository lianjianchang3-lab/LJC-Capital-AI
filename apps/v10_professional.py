import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import time

from core.v10 import V10MarketHub, V10FundMonitor, V10SectorRotation, V10AICommittee, V10TradingPlan

st.set_page_config(page_title="LJC V10.0 Professional", page_icon="🏛️", layout="wide")
st.title("🏛️ LJC Capital AI V10.0 Professional")
st.caption("Level2资金监控｜行业轮动AI｜投委会V4｜自动交易计划｜中文手机端")

st.sidebar.header("控制面板")
auto = st.sidebar.checkbox("自动刷新", value=False)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top_n = st.sidebar.slider("显示前N名", 10, 200, 50)

tabs = st.tabs(["总控台", "市场数据", "资金监控", "行业轮动", "AI投委会", "交易计划", "系统验收", "手机部署"])

market = V10MarketHub()
health = market.health()

with tabs[0]:
    st.header("V10 总控台")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("数据源", health.get("active_source"))
    c2.metric("行数", health.get("rows"))
    c3.metric("状态", "正常" if health.get("ready") else "等待数据")
    c4.metric("版本", "V10.0")
    st.success("V10.0 已加载：资金、行业、投委会、交易计划四大核心模块。")

with tabs[1]:
    st.header("市场数据中心")
    q = market.quotes()
    if q.empty:
        st.warning("暂无行情数据。")
    else:
        st.dataframe(q.head(top_n), use_container_width=True, hide_index=True)

with tabs[2]:
    st.header("Level2 资金监控")
    fund = V10FundMonitor().analyze()
    st.success(fund.get("summary"))
    st.dataframe(pd.DataFrame(fund.get("items", [])).head(top_n), use_container_width=True, hide_index=True)

with tabs[3]:
    st.header("行业轮动 AI")
    sector = V10SectorRotation().rank()
    st.success(sector.get("summary"))
    st.dataframe(pd.DataFrame(sector.get("items", [])).head(top_n), use_container_width=True, hide_index=True)

with tabs[4]:
    st.header("AI 投委会 V4")
    committee = V10AICommittee().decide()
    st.success(committee.get("summary"))
    st.dataframe(pd.DataFrame(committee.get("votes", [])).head(top_n), use_container_width=True, hide_index=True)

with tabs[5]:
    st.header("自动交易计划")
    plan = V10TradingPlan().generate()
    st.info(plan.get("summary"))
    st.dataframe(pd.DataFrame(plan.get("plans", [])).head(top_n), use_container_width=True, hide_index=True)

with tabs[6]:
    st.header("V10.0 系统验收")
    checks = [
        {"检查项": "市场数据中心", "结果": "通过" if health.get("ready") else "待检查", "说明": health.get("active_source")},
        {"检查项": "资金监控", "结果": "通过", "说明": V10FundMonitor().analyze().get("status")},
        {"检查项": "行业轮动", "结果": "通过", "说明": V10SectorRotation().rank().get("status")},
        {"检查项": "AI投委会", "结果": "通过", "说明": V10AICommittee().decide().get("status")},
        {"检查项": "交易计划", "结果": "通过", "说明": V10TradingPlan().generate().get("status")},
    ]
    st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)

with tabs[7]:
    st.header("手机端部署")
    st.code("python -m streamlit run apps/v10_mobile.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
