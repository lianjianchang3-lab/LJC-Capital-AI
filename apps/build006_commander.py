import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.build006 import Build006Commander

st.set_page_config(page_title="LJC Build006 AI Commander", page_icon="🤖", layout="wide")
st.title("🤖 LJC Capital AI Pro Build 006")
st.caption("AI指挥中心｜LJC评分｜主升浪识别｜交易计划｜手机实战面板")

cmd = Build006Commander()

st.sidebar.header("控制")
auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N", 8, 100, 30)

tabs = st.tabs(["AI指挥中心","LJC评分","主升浪","交易计划","健康检查","手机部署"])

with tabs[0]:
    d = cmd.dashboard()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("AI市场评分", d.get("market_score"))
    c2.metric("建议仓位", d.get("position"))
    c3.metric("风险等级", d.get("risk"))
    c4.metric("买入关注", d.get("buy_count"))
    st.success(d.get("summary"))
    st.subheader("今日重点机会")
    st.dataframe(pd.DataFrame(d.get("top",[])).head(top), use_container_width=True, hide_index=True)

with tabs[1]:
    df = cmd.ljc_score()
    st.dataframe(df.head(top), use_container_width=True, hide_index=True)

with tabs[2]:
    df = cmd.ljc_score()
    if not df.empty:
        show = df[["code","name","price","change_pct","LJC评分","星级","主升浪阶段","操作建议","建议仓位"]].head(top)
        st.dataframe(show, use_container_width=True, hide_index=True)

with tabs[3]:
    plan = cmd.trading_plan()
    st.dataframe(pd.DataFrame(plan.get("plans",[])), use_container_width=True, hide_index=True)

with tabs[4]:
    from core.multisource import MultiSourceRealtimeHub
    st.json(MultiSourceRealtimeHub().health())

with tabs[5]:
    st.code("python -m streamlit run apps/build006_mobile.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
