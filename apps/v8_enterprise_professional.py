import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st
from core.enterprise import EnterpriseCommander
from core.professional import LCRIPro, InstitutionCenter

st.set_page_config(page_title="LJC V8 Enterprise Pro", page_icon="🚀", layout="wide")
st.title("🚀 LJC Capital AI Pro V8.0 Enterprise Professional")
st.caption("Institution Center｜LCRI Pro｜Execution Board｜Unified Commander")

@st.cache_data(ttl=8)
def load_all():
    snap = EnterpriseCommander().snapshot()
    lcri = LCRIPro().dataframe()
    inst_center = InstitutionCenter()
    inst = inst_center.dataframe()
    inst_summary = inst_center.summary()
    execution = LCRIPro().execution_text(12)
    return snap, lcri, inst, inst_summary, execution

snap, lcri_df, inst_df, inst_sum, execution = load_all()
market = snap.get("market", {}) or {}
health = snap.get("radar_health", {}) or {}

auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N", 5, 80, 30)

m1,m2,m3,m4,m5 = st.columns(5)
m1.metric("市场", market.get("state", "-"))
m2.metric("仓位", market.get("position", "-"))
m3.metric("LCRI均分", market.get("lcri_avg", "-"))
m4.metric("扫描", health.get("lcri_count", 0))
m5.metric("机构热度", inst_sum.get("avg_heat", "-"))

st.success(snap.get("summary","-"))
st.info(inst_sum.get("summary","-"))

tabs = st.tabs(["总控执行", "LCRI Pro", "机构资金中心", "风险与回避", "今日计划", "系统"])

def show(df, cols=None):
    if df is None or df.empty:
        st.warning("暂无数据")
        return
    if cols:
        use = [c for c in cols if c in df.columns]
        if use:
            df = df[use]
    st.dataframe(df.head(top), use_container_width=True, hide_index=True)

with tabs[0]:
    cols = ["code","name","V8动作","V8综合分","胜率估算","V8仓位","第一买点","第二买点","止损价","第一止盈","第二止盈","风险等级","V8理由"]
    show(lcri_df, cols)

with tabs[1]:
    show(lcri_df)

with tabs[2]:
    show(inst_df)

with tabs[3]:
    risk = lcri_df.copy() if not lcri_df.empty else pd.DataFrame()
    if not risk.empty:
        risk = risk.sort_values(["风险等级","V8综合分"], ascending=[False, True])
    show(risk, ["code","name","V8动作","风险等级","risk_score","V8综合分","LCRI Score","V8理由"])

with tabs[4]:
    st.text(execution)

with tabs[5]:
    st.json({"market": market, "radar_health": health, "institution_summary": inst_sum, "services": snap.get("services", []), "configs": snap.get("configs", {})})

if auto:
    time.sleep(sec)
    st.rerun()
