import streamlit as st
import pandas as pd

from core import LJCAppCore
from core.data_center import DataCenter
from core.capital import CapitalEngine
from core.lia import LIAEngine
from core.decision import DecisionEngine
from core.portfolio import PortfolioEngine
from updater import UpdateService

core = LJCAppCore()
boot = core.boot()
dc = DataCenter()
capital_engine = CapitalEngine(dc)
lia_engine = LIAEngine(dc)
decision_engine = DecisionEngine(lia_engine)
portfolio_engine = PortfolioEngine(lia_engine=lia_engine)
updater = UpdateService()

plan = decision_engine.make_plan()
signals = plan.get("signals", [])

st.set_page_config(page_title="LJC Capital AI Pro V8", page_icon="🚀", layout="wide")

st.title("🚀 LJC Capital AI Pro V8.0")
st.caption("Build005-008｜LIA / Decision / Portfolio / OTA")

with st.container(border=True):
    st.subheader("今日作战计划")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("市场", plan["market"])
    c2.metric("建议仓位", plan["position"])
    c3.metric("风险", plan["risk"])
    c4.metric("版本", boot["version"])
    st.write(plan["summary"])

tab1, tab2, tab3, tab4 = st.tabs(["今日决策", "LIA排行", "我的持仓", "更新中心"])

with tab1:
    st.subheader("💎 Diamond")
    for s in plan["diamond"]:
        with st.container(border=True):
            st.markdown(f"### {s.code} {s.name}｜LIA {s.lia}")
            a, b, c, d = st.columns(4)
            a.metric("资金", s.capital)
            b.metric("趋势", s.trend)
            c.metric("板块", s.sector)
            d.metric("可信度", s.confidence)
            st.write(s.action)
            st.caption(s.explanation)

    st.subheader("🚀 Opportunity")
    for s in plan["opportunity"]:
        st.write(f"{s.code} {s.name}｜LIA {s.lia}｜{s.action}")

    st.subheader("👀 Watch")
    for s in plan["watch"]:
        st.write(f"{s.code} {s.name}｜LIA {s.lia}｜{s.action}")

with tab2:
    rows = [{
        "代码": s.code,
        "名称": s.name,
        "LIA": s.lia,
        "资金": s.capital,
        "趋势": s.trend,
        "板块": s.sector,
        "风险安全": s.risk,
        "可信度": s.confidence,
        "评级": s.rank,
        "建议": s.action,
        "说明": s.explanation,
    } for s in signals]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

with tab3:
    st.dataframe(portfolio_engine.analyze(), use_container_width=True, hide_index=True)
    st.caption("可编辑 data/portfolio.csv 来维护真实持仓。")

with tab4:
    status = updater.check()
    st.write(status)
    st.caption("Build008 已建立 OTA 框架；当前为手动安全模式。")
    if st.button("手动拉取 develop 更新"):
        st.code(updater.pull())

st.subheader("V8.0 Progress")
st.progress(0.72)
st.write("Build005 LIA Engine ✅ | Build006 Decision ✅ | Build007 Portfolio ✅ | Build008 OTA Framework ✅")
