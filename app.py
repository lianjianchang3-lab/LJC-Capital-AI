import streamlit as st
import pandas as pd

from core import LJCAppCore
from core.data_center import DataCenter
from core.capital import CapitalEngine
from core.lia import LIAEngine
from core.decision import DecisionEngine
from core.portfolio import PortfolioEngine
from core.data_import import InboxImporter
from updater import UpdateService

core = LJCAppCore()
boot = core.boot()
dc = DataCenter()
lia_engine = LIAEngine(dc)
decision_engine = DecisionEngine(lia_engine)
portfolio_engine = PortfolioEngine(lia_engine=lia_engine)
updater = UpdateService()
importer = InboxImporter()

plan = decision_engine.make_plan()
signals = plan.get("signals", [])

st.set_page_config(page_title="LJC Capital AI Pro V8 RC1", page_icon="🚀", layout="wide")

st.title("🚀 LJC Capital AI Pro V8.0 RC1")
st.caption("真实数据 Inbox｜LIA｜今日作战计划")

with st.container(border=True):
    st.subheader("今日作战计划")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("市场", plan["market"])
    c2.metric("建议仓位", plan["position"])
    c3.metric("风险", plan["risk"])
    c4.metric("版本", boot["version"])
    st.write(plan["summary"])

tab1, tab2, tab3, tab4, tab5 = st.tabs(["今日决策", "LIA排行", "我的持仓", "真实数据导入", "更新中心"])

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
    st.caption("真实持仓可放入 data/inbox/，文件名包含 portfolio 或 持仓。")

with tab4:
    st.subheader("真实数据导入")
    st.write("把同花顺 / Moomoo / 持仓 CSV 放入：")
    st.code("data/inbox/")
    st.write("系统会自动识别：行情、资金、持仓。")
    if st.button("导入 inbox CSV 并刷新数据"):
        result = importer.import_all()
        st.write(result)
        st.success("导入完成。请刷新页面查看最新分析。")

    st.caption("导入后文件会移动到 data/processed/，避免重复导入。")

with tab5:
    status = updater.check()
    st.write(status)
    if st.button("手动拉取 develop 更新"):
        st.code(updater.pull())

st.subheader("V8.0 Progress")
st.progress(0.82)
st.write("RC1：真实数据导入已安装。下一步：数据模板与模型校准。")
