import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

from core.enterprise import EnterpriseCommander

st.set_page_config(page_title="LJC V7 Enterprise Hub", page_icon="🧭", layout="wide")
st.title("🧭 LJC Capital AI Pro V7 Enterprise Hub")
st.caption("统一入口｜DecisionHub｜Market Radar｜复用现有 V5/V5.1 模块")

auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N", 5, 50, 20)

cmd = EnterpriseCommander()
snap = cmd.snapshot()

tabs = st.tabs(["总控台", "LCRI Top", "AI Trader Top", "机构共振 Top", "风险雷达", "配置与服务"])

with tabs[0]:
    market = snap.get("market", {})
    health = snap.get("radar_health", {})
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("市场状态", market.get("state"))
    c2.metric("LCRI均分", market.get("lcri_avg"))
    c3.metric("建议仓位", market.get("position"))
    c4.metric("扫描数", health.get("lcri_count"))
    st.success(snap.get("summary"))
    st.json(health)

with tabs[1]:
    st.dataframe(pd.DataFrame(snap.get("lcri_top", [])).head(top), use_container_width=True, hide_index=True)

with tabs[2]:
    st.dataframe(pd.DataFrame(snap.get("trader_top", [])).head(top), use_container_width=True, hide_index=True)

with tabs[3]:
    st.dataframe(pd.DataFrame(snap.get("institution_top", [])).head(top), use_container_width=True, hide_index=True)

with tabs[4]:
    st.dataframe(pd.DataFrame(snap.get("risk_top", [])).head(top), use_container_width=True, hide_index=True)

with tabs[5]:
    st.subheader("已挂载服务")
    st.write(snap.get("services"))
    st.subheader("配置状态")
    st.json(snap.get("configs"))

if auto:
    time.sleep(sec)
    st.rerun()
