import streamlit as st
import pandas as pd

from core.institutional import InstitutionCapitalMatrix, MarketBreadthPro, PortfolioAIV4, InvestmentOS
from core.quant import QuantEngine
from core.macro import MacroAllocationEngine
from core.reports_pro import ReportCenterPro

st.set_page_config(page_title="LJC Institutional OS", page_icon="🏦", layout="wide")

st.title("🏦 LJC Capital AI V8.1 Institutional OS")
st.caption("Build201-400｜机构资金矩阵｜市场宽度｜组合AI｜量化因子｜宏观配置｜机构日报")

os_engine = InvestmentOS()

tabs = st.tabs([
    "Investment OS",
    "Capital Matrix",
    "Market Breadth Pro",
    "Portfolio AI V4",
    "Quant Engine",
    "Macro Allocation",
    "Institution Report",
    "Build201-400 Validation"
])

with tabs[0]:
    st.header("Build281-300 Investment OS")
    d = os_engine.dashboard()
    a,b,c,dcol = st.columns(4)
    a.metric("Market", d["commander"].get("market", {}).get("regime"))
    b.metric("Position", d["commander"].get("suggested_total_position"))
    c.metric("Breadth", d["breadth"].get("breadth_pct"))
    dcol.metric("Institution Avg", d["capital"].get("avg_institution_score"))
    st.success(d.get("final"))
    st.warning(d.get("warning"))

with tabs[1]:
    st.header("Build201-220 Institution Capital Matrix")
    cap = InstitutionCapitalMatrix().analyze()
    st.metric("Avg Institution Score", cap.get("avg_institution_score"))
    st.dataframe(pd.DataFrame(cap.get("matrix", [])), use_container_width=True, hide_index=True)

with tabs[2]:
    st.header("Build221-240 Market Breadth Pro")
    st.json(MarketBreadthPro().snapshot())

with tabs[3]:
    st.header("Build241-260 Portfolio AI V4")
    st.json(PortfolioAIV4().analyze())

with tabs[4]:
    st.header("Build301-320 Professional Quant Engine")
    st.dataframe(QuantEngine().factors(), use_container_width=True, hide_index=True)

with tabs[5]:
    st.header("Build321-340 Macro Allocation Engine")
    st.json(MacroAllocationEngine().allocate())

with tabs[6]:
    st.header("Build381-400 Institution Report Center")
    st.code(ReportCenterPro().markdown(), language="markdown")

with tabs[7]:
    st.header("Build201-400 Validation")
    st.success("Institutional OS 模块已加载。")
    st.write("说明：本应用是模块化独立入口，不破坏原 app.py。")
    st.code("streamlit run apps/institutional_os.py")
