import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st
from core.enterprise import EnterpriseCommander
from core.execution import ExecutionCenter
from core.professional import LCRIExplain, InstitutionCenter

st.set_page_config(page_title="LJC V8.5 Execution Center", page_icon="🎯", layout="wide")
st.title("🎯 LJC Capital AI Pro V8.5 Execution Center")
st.caption("AI执行中心｜LCRI解释引擎｜机构驾驶舱｜手机交易助手")

@st.cache_data(ttl=8)
def load_all():
    snap = EnterpriseCommander().snapshot()
    exe = ExecutionCenter()
    exe_df = exe.dataframe()
    exp_df = LCRIExplain().dataframe() if LCRIExplain else pd.DataFrame()
    inst = InstitutionCenter()
    return snap, exe_df, exe.text(12), exp_df, inst.dataframe(), inst.summary()

snap, exe_df, exe_text, explain_df, inst_df, inst_summary = load_all()
market = snap.get("market", {}) or {}
health = snap.get("radar_health", {}) or {}

auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N", 5, 80, 30)

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("市场", market.get("state","-"))
c2.metric("仓位", market.get("position","-"))
c3.metric("LCRI均分", market.get("lcri_avg","-"))
c4.metric("扫描数", health.get("lcri_count",0))
c5.metric("机构热度", inst_summary.get("avg_heat","-"))
st.success(snap.get("summary","-"))
st.info(inst_summary.get("summary","-"))

tabs = st.tabs(["AI执行中心","LCRI解释","机构驾驶舱","今日计划","风险检查","系统"])

def show(df, cols=None):
    if df is None or df.empty:
        st.warning("暂无数据"); return
    if cols:
        use = [c for c in cols if c in df.columns]
        if use: df = df[use]
    st.dataframe(df.head(top), use_container_width=True, hide_index=True)

with tabs[0]:
    show(exe_df, ["code","name","V8动作","买入优先级","V8综合分","首次建仓","最大允许仓位","风险预算","建议持有天数","第一买点","第二买点","突破确认价","止损价","第一止盈","第二止盈","执行结论"])
with tabs[1]:
    show(explain_df, ["code","name","V8动作","V8综合分","推荐原因","风险原因","解释文本"])
with tabs[2]:
    show(inst_df, ["code","name","V8机构热度","资金状态","机构评级","机构共振指数","北向模拟分","龙虎榜模拟分","基金关注分"])
with tabs[3]:
    st.text(exe_text)
with tabs[4]:
    risk = exe_df.copy() if exe_df is not None and not exe_df.empty else pd.DataFrame()
    if not risk.empty: risk = risk.sort_values(["买入优先级","risk_score"], ascending=[False, True])
    show(risk, ["code","name","V8动作","买入优先级","风险预算","risk_score","V8综合分","减仓条件","执行结论"])
with tabs[5]:
    st.json({"market":market,"radar_health":health,"institution_summary":inst_summary,"services":snap.get("services",[]),"configs":snap.get("configs",{})})

if auto:
    time.sleep(sec)
    st.rerun()
