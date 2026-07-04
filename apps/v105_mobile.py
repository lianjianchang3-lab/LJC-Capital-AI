import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

import streamlit as st
import pandas as pd
from core.v105 import LiveHub105, CommitteeV5, PortfolioEngine105, SectorEngine105, LCRIEngine105

st.set_page_config(page_title="LJC V10.5 手机端", page_icon="📱", layout="centered")
st.title("📱 LJC V10.5 手机投委会")
st.caption("一屏看市场｜资金｜行业｜交易计划")

h=LiveHub105().health(); p=PortfolioEngine105().optimize()
c1,c2=st.columns(2)
c1.metric("数据源",h["active_source"]); c2.metric("行数",h["rows"])
st.metric("建议现金", f"{p['cash_weight']:.0%}")
st.success(p["summary"])

d=CommitteeV5().decide()
st.subheader("AI投委会")
for v in d.get("votes", [])[:10]:
    text=f"{v['星级']}｜{v['最终决策']}｜{v['代码']} {v['名称']}｜仓位 {v['建议仓位']}"
    if v["最终决策"] in ["重点买入关注","买入观察"]:
        st.success(text)
    elif v["最终决策"]=="风险回避":
        st.error(text)
    else:
        st.info(text)
    st.caption(v["理由"])

with st.expander("行业轮动Top"):
    st.dataframe(pd.DataFrame(SectorEngine105().rank().get("items",[])).head(10), use_container_width=True, hide_index=True)
with st.expander("LCRI资金Top"):
    st.dataframe(pd.DataFrame(LCRIEngine105().calculate().get("items",[])).head(10), use_container_width=True, hide_index=True)
