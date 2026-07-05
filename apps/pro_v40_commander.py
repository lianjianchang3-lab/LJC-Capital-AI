import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.pro_v40 import V40Commander, UnifiedAIEngine, InstitutionSignalCenter, PositionController, LearningCenter

st.set_page_config(page_title="LJC Pro V4 Commander", page_icon="🧭", layout="wide")
st.title("🧭 LJC Capital AI Pro V4.0 Unified Commander")
st.caption("统一AI引擎｜机构信号中心｜仓位控制器｜学习中心｜实盘驾驶舱")

auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N", 5, 100, 30)

tabs = st.tabs(["实盘驾驶舱", "统一AI引擎", "机构信号", "仓位控制", "学习中心", "手机部署"])

with tabs[0]:
    d = V40Commander().dashboard()
    s = d["state"]
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("市场状态", s.get("state"))
    c2.metric("AI评分", s.get("ai_score"))
    c3.metric("建议仓位", s.get("position"))
    c4.metric("风险", s.get("risk"))
    st.success(s.get("summary"))
    st.subheader("今日机构信号")
    st.dataframe(pd.DataFrame(d["signals"]).head(top), use_container_width=True, hide_index=True)

with tabs[1]:
    st.dataframe(UnifiedAIEngine().run().head(top), use_container_width=True, hide_index=True)

with tabs[2]:
    st.dataframe(InstitutionSignalCenter().signals().head(top), use_container_width=True, hide_index=True)

with tabs[3]:
    a = PositionController().allocation()
    st.success(a.get("summary"))
    st.dataframe(pd.DataFrame(a.get("items",[])), use_container_width=True, hide_index=True)

with tabs[4]:
    lc = LearningCenter()
    if st.button("记录当前AI建议快照"):
        n = lc.snapshot()
        st.success(f"已记录 {n} 条建议")
    st.json(lc.stats())
    st.dataframe(lc.read(), use_container_width=True, hide_index=True)

with tabs[5]:
    st.code("python -m streamlit run apps/pro_v40_mobile.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
