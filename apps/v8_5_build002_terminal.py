import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st
from core.enterprise import EnterpriseCommander
from core.execution import ExecutionCenter
from core.portfolio_center import PortfolioCenter
from core.watchlist_center import WatchlistCenter
from core.daily_plan import DailyPlan

st.set_page_config(page_title="LJC V8.5 Build002", page_icon="💼", layout="wide")
st.title("💼 LJC V8.5 Build002｜Portfolio + Watchlist + Daily Plan")

@st.cache_data(ttl=8)
def load_all():
    snap = EnterpriseCommander().snapshot()
    exe = ExecutionCenter().dataframe()
    pf_center = PortfolioCenter()
    pf = pf_center.analyze()
    pf_summary = pf_center.summary()
    wl_center = WatchlistCenter()
    wl = wl_center.analyze()
    wl_summary = wl_center.summary()
    plan = DailyPlan().generate()
    return snap, exe, pf, pf_summary, wl, wl_summary, plan

snap, exe, pf, pf_summary, wl, wl_summary, plan = load_all()
market = snap.get("market", {}) or {}

auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N", 5, 80, 30)

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("市场", market.get("state","-"))
c2.metric("建议仓位", market.get("position","-"))
c3.metric("LCRI均分", market.get("lcri_avg","-"))
c4.metric("持仓市值", pf_summary.get("total_value","-"))
c5.metric("自选重点", wl_summary.get("focus","-"))

st.success(plan.get("text","").split("\n")[0] if plan else "-")
st.info(pf_summary.get("summary","-") + "｜" + wl_summary.get("summary","-"))

tabs = st.tabs(["每日计划","执行中心","我的持仓","自选股","风险持仓","系统"])

def show(df, cols=None):
    if df is None or df.empty:
        st.warning("暂无数据"); return
    if cols:
        use = [c for c in cols if c in df.columns]
        if use: df = df[use]
    st.dataframe(df.head(top), use_container_width=True, hide_index=True)

with tabs[0]:
    st.text(plan.get("text","暂无计划"))
with tabs[1]:
    show(exe, ["code","name","V8动作","买入优先级","首次建仓","最大允许仓位","风险预算","建议持有天数","执行结论"])
with tabs[2]:
    show(pf, ["code","name","shares","cost","price","市值","浮盈浮亏","浮盈浮亏%","持仓建议","组合操作","V8综合分","买入优先级"])
    st.caption("持仓文件：data/portfolio/holdings.csv，可自行编辑 code,name,shares,cost")
with tabs[3]:
    show(wl, ["code","name","自选状态","V8动作","买入优先级","V8综合分","首次建仓","最大允许仓位","执行结论"])
with tabs[4]:
    risk = pf.copy() if pf is not None and not pf.empty else pd.DataFrame()
    if not risk.empty:
        risk = risk[risk["持仓建议"].astype(str).str.contains("止损|减仓|回避", na=False)]
    show(risk)
with tabs[5]:
    st.json({"market": market, "portfolio": pf_summary, "watchlist": wl_summary, "services": snap.get("services", [])})

if auto:
    time.sleep(sec)
    st.rerun()
