import sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

import streamlit as st
import pandas as pd
from core.v11 import DataCenterV11,MarketCenterV11,AICenterV11,PortfolioCenterV11,RiskCenterV11,StrategyCenterV11,ReportCenterV11,SystemCenterV11

st.set_page_config(page_title="LJC V11 RC", page_icon="🏦", layout="wide")
st.title("🏦 LJC Capital AI V11 RC")
st.caption("数据中心｜市场中心｜AI中心｜组合中心｜风险中心｜策略中心｜报告中心｜系统中心")

auto=st.sidebar.checkbox("自动刷新",False)
sec=st.sidebar.slider("刷新秒数",10,120,30)
top=st.sidebar.slider("显示前N名",10,200,50)
tabs=st.tabs(["总控台","数据中心","市场中心","AI中心","组合中心","风险中心","策略中心","报告中心","系统中心","手机部署"])

with tabs[0]:
    h=DataCenterV11().health(); p=PortfolioCenterV11().plan(); r=RiskCenterV11().assess()
    c1,c2,c3,c4=st.columns(4)
    c1.metric("数据源",h["active_source"]); c2.metric("行数",h["rows"]); c3.metric("建议现金",f"{p['cash_weight']:.0%}"); c4.metric("组合风险",r.get("portfolio_risk"))
    st.success(p["summary"])

with tabs[1]:
    st.json(DataCenterV11().health()); st.json(DataCenterV11().quality()); st.dataframe(DataCenterV11().quotes().head(top), use_container_width=True, hide_index=True)
with tabs[2]:
    m=MarketCenterV11().snapshot(); st.success(m.get("summary")); st.dataframe(pd.DataFrame(m.get("hot_sectors",[])), use_container_width=True, hide_index=True); st.dataframe(pd.DataFrame(m.get("leaders",[])).head(top), use_container_width=True, hide_index=True)
with tabs[3]:
    ai=AICenterV11().decisions(); st.success(ai.get("summary")); st.dataframe(pd.DataFrame(ai.get("items",[])).head(top), use_container_width=True, hide_index=True)
with tabs[4]:
    st.json(PortfolioCenterV11().plan())
with tabs[5]:
    risk=RiskCenterV11().assess(); st.warning(risk.get("summary")); st.dataframe(pd.DataFrame(risk.get("items",[])).head(top), use_container_width=True, hide_index=True)
with tabs[6]:
    st.dataframe(pd.DataFrame(StrategyCenterV11().registry().get("strategies",[])), use_container_width=True, hide_index=True)
with tabs[7]:
    st.code(ReportCenterV11().markdown(), language="markdown")
with tabs[8]:
    st.json(SystemCenterV11().status())
with tabs[9]:
    st.code("python -m streamlit run apps/v11_mobile.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec); st.rerun()
