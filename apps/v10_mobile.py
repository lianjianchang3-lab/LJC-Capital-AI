import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd

from core.v10 import V10MarketHub, V10AICommittee, V10TradingPlan, V10SectorRotation

st.set_page_config(page_title="LJC V10 手机端", page_icon="📱", layout="centered")
st.title("📱 LJC V10.0 手机投委会")
st.caption("AI结论｜交易计划｜行业轮动｜风险提示")

h = V10MarketHub().health()
committee = V10AICommittee().decide()
plan = V10TradingPlan().generate()
sector = V10SectorRotation().rank()

st.subheader("今日状态")
c1, c2 = st.columns(2)
c1.metric("数据源", h.get("active_source"))
c2.metric("行数", h.get("rows"))

st.subheader("AI投委会结论")
st.success(committee.get("summary"))

votes = committee.get("votes", [])
if votes:
    for v in votes[:8]:
        text = f"{v['最终决策']}｜{v['代码']} {v['名称']}｜票数 {v['投票数']}｜仓位 {v['建议仓位']}"
        if v["最终决策"] == "买入关注":
            st.success(text)
        elif v["最终决策"] == "减仓/回避":
            st.error(text)
        else:
            st.info(text)
        st.caption(v.get("理由"))

st.subheader("交易计划")
plans = plan.get("plans", [])
if plans:
    st.dataframe(pd.DataFrame(plans[:10]), use_container_width=True, hide_index=True)

st.subheader("行业轮动")
items = sector.get("items", [])
if items:
    st.dataframe(pd.DataFrame(items[:10]), use_container_width=True, hide_index=True)
