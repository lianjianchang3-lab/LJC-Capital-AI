import sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

import streamlit as st
import pandas as pd
from core.v105 import LiveHub105,LCRIEngine105,SectorEngine105,CommitteeV5,PortfolioEngine105,RiskEngine105

st.set_page_config(page_title="LJC V10.5 One-Click", page_icon="🚀", layout="wide")
st.title("🚀 LJC Capital AI V10.1-10.5 一键部署版")
st.caption("实时行情｜LCRI资金｜行业轮动｜投委会V5｜风险仓位｜手机同步")

auto=st.sidebar.checkbox("自动刷新", False)
sec=st.sidebar.slider("刷新秒数",10,120,30)
top=st.sidebar.slider("显示前N名",10,200,50)

tabs=st.tabs(["总控台","实时行情","LCRI资金","行业轮动","AI投委会V5","风险与仓位","一键验收","手机部署"])

with tabs[0]:
    h=LiveHub105().health(); p=PortfolioEngine105().optimize()
    c1,c2,c3,c4=st.columns(4)
    c1.metric("数据源",h["active_source"]); c2.metric("行数",h["rows"]); c3.metric("实时", "ON" if h["live_ready"] else "备用"); c4.metric("现金", f"{p['cash_weight']:.0%}")
    st.success(p["summary"])

with tabs[1]:
    q=LiveHub105().quotes()
    st.dataframe(q.head(top), use_container_width=True, hide_index=True)

with tabs[2]:
    r=LCRIEngine105().calculate()
    st.success(r["summary"])
    st.dataframe(pd.DataFrame(r["items"]).head(top), use_container_width=True, hide_index=True)

with tabs[3]:
    s=SectorEngine105().rank()
    st.success(s["summary"])
    st.dataframe(pd.DataFrame(s["items"]).head(top), use_container_width=True, hide_index=True)

with tabs[4]:
    d=CommitteeV5().decide()
    st.success(d["summary"])
    st.dataframe(pd.DataFrame(d["votes"]).head(top), use_container_width=True, hide_index=True)

with tabs[5]:
    risk=RiskEngine105().assess(); port=PortfolioEngine105().optimize()
    st.info(port["summary"])
    st.dataframe(pd.DataFrame(risk["items"]).head(top), use_container_width=True, hide_index=True)

with tabs[6]:
    h=LiveHub105().health()
    checks=[
        {"检查项":"实时数据中心","结果":"通过" if h["rows"]>0 else "待检查","说明":h["active_source"]},
        {"检查项":"LCRI资金","结果":LCRIEngine105().calculate()["status"],"说明":"资金模型"},
        {"检查项":"行业轮动","结果":SectorEngine105().rank()["status"],"说明":"行业热度"},
        {"检查项":"投委会V5","结果":CommitteeV5().decide()["status"],"说明":"AI决策"},
        {"检查项":"组合风控","结果":PortfolioEngine105().optimize()["status"],"说明":"仓位现金"},
    ]
    st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)

with tabs[7]:
    st.code("python -m streamlit run apps/v105_mobile.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
