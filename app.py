import streamlit as st
import pandas as pd
from core import LJCAppCore
from core.data_center import DataCenter
from core.capital import CapitalEngine

core = LJCAppCore()
boot = core.boot()
dc = DataCenter()
capital_engine = CapitalEngine(dc)
health = dc.health_check()
signals = capital_engine.analyze_all()

st.set_page_config(page_title="LJC Capital AI Pro V8", page_icon="🚀", layout="wide")

st.title("🚀 LJC Capital AI Pro V8.0")
st.caption("Build003 Capital Engine｜资金健康 / 机构评分 / 吸筹阶段")

with st.container(border=True):
    st.subheader("System Status")
    c1, c2, c3 = st.columns(3)
    c1.metric("Version", boot["version"])
    c2.metric("Data Quality", health["overall_score"])
    c3.metric("Capital Signals", len(signals))

st.subheader("🧠 Capital Engine")
rows = []
for s in signals:
    rows.append({
        "代码": s.code,
        "名称": s.name,
        "资金健康": s.capital_health,
        "机构评分": s.institution_score,
        "可信度": s.confidence,
        "阶段": s.stage,
        "趋势": s.trend,
        "连续性": s.continuity_stars,
        "主力净流入(亿)": s.net_main,
        "说明": s.explanation,
    })

df = pd.DataFrame(rows)
if not df.empty:
    df = df.sort_values(["资金健康", "可信度"], ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("Diamond / Opportunity / Watch")
for s in signals:
    if s.capital_health >= 90:
        bucket = "💎 Diamond Core"
    elif s.capital_health >= 75:
        bucket = "🚀 Opportunity"
    else:
        bucket = "👀 Watch"

    with st.container(border=True):
        st.markdown(f"### {bucket}｜{s.code} {s.name}")
        a, b, c, d = st.columns(4)
        a.metric("资金健康", s.capital_health)
        b.metric("机构评分", s.institution_score)
        c.metric("可信度", s.confidence)
        d.metric("阶段", s.stage)
        st.caption(f"趋势：{s.trend}｜连续性：{s.continuity_stars}")
        st.write(s.explanation)

with st.expander("Data Center 原始数据"):
    st.write("Capital")
    st.dataframe(dc.get_capital().data, use_container_width=True)
    st.write("Quotes")
    st.dataframe(dc.get_quotes().data, use_container_width=True)

st.subheader("V8.0 Progress")
st.progress(0.32)
st.write("Build003 Capital Engine: 已安装")
st.write("下一步：Build004 LIA Engine")
