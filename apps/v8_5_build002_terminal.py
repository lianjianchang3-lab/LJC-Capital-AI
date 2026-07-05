import sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

from core.enterprise import EnterpriseCommander
from core.execution import ExecutionCenter
from core.portfolio_center import PortfolioCenter
from core.watchlist_center import WatchlistCenter

st.set_page_config(page_title="LJC V8.5 Build002 Stable", page_icon="💼", layout="wide")
st.title("💼 LJC V8.5 Build002｜Portfolio + Watchlist + Daily Plan")
st.caption("已修复 load_all 卡住问题；自选股中心可新增股票：scripts/start_v8_5_watchlist_center.command")

auto = st.sidebar.checkbox("自动刷新", False)
sec = st.sidebar.slider("刷新秒数", 15, 180, 60)
top = st.sidebar.slider("显示前N", 5, 80, 30)

def safe_call(label, fn, default):
    try:
        return fn()
    except Exception as e:
        st.sidebar.warning(f"{label} 异常：{e}")
        return default

snap = safe_call("Commander", lambda: EnterpriseCommander().snapshot(), {})
market = snap.get("market", {}) or {}

exe = safe_call("Execution", lambda: ExecutionCenter().dataframe(), pd.DataFrame())
pf_center = PortfolioCenter()
pf = safe_call("Portfolio", lambda: pf_center.analyze(), pd.DataFrame())
pf_summary = safe_call("PortfolioSummary", lambda: pf_center.summary(), {"summary": "暂无持仓", "total_value": 0, "pnl": 0, "risk_count": 0})

wl_center = WatchlistCenter()
wl = safe_call("Watchlist", lambda: wl_center.analyze(), pd.DataFrame())
wl_summary = safe_call("WatchlistSummary", lambda: wl_center.summary(), {"summary": "暂无自选股", "focus": 0, "avoid": 0})

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("市场", market.get("state","-"))
c2.metric("建议仓位", market.get("position","-"))
c3.metric("LCRI均分", market.get("lcri_avg","-"))
c4.metric("持仓市值", pf_summary.get("total_value","-"))
c5.metric("自选重点", wl_summary.get("focus","-"))

st.success((snap.get("summary") or "系统已启动"))
st.info(pf_summary.get("summary","-") + "｜" + wl_summary.get("summary","-"))

tabs = st.tabs(["每日计划","执行中心","我的持仓","自选股","风险持仓","系统"])

def show(df, cols=None):
    if df is None or df.empty:
        st.warning("暂无数据")
        return
    if cols:
        use = [c for c in cols if c in df.columns]
        if use:
            df = df[use]
    st.dataframe(df.head(top), use_container_width=True, hide_index=True)

def daily_plan_text():
    lines = ["LJC V8.5 每日交易计划", "=" * 28]
    lines.append(f"市场：{market.get('state','-')}｜建议仓位：{market.get('position','-')}｜LCRI均分：{market.get('lcri_avg','-')}")
    lines.append("")
    lines.append("今日买入/关注：")
    if exe is None or exe.empty:
        lines.append("- 暂无")
    else:
        buy = exe[exe["买入优先级"] <= 3].head(5) if "买入优先级" in exe.columns else exe.head(5)
        if buy.empty:
            lines.append("- 暂无")
        else:
            for _, r in buy.iterrows():
                lines.append(f"- {r.get('code')} {r.get('name')}｜优先级{r.get('买入优先级')}｜首仓{r.get('首次建仓')}｜最大{r.get('最大允许仓位')}")
    lines.append("")
    lines.append("今日减仓/风险：")
    if pf is None or pf.empty or "持仓建议" not in pf.columns:
        lines.append("- 暂无")
    else:
        risk = pf[pf["持仓建议"].astype(str).str.contains("止损|减仓|回避", na=False)].head(5)
        if risk.empty:
            lines.append("- 暂无")
        else:
            for _, r in risk.iterrows():
                lines.append(f"- {r.get('code')} {r.get('name')}｜{r.get('持仓建议')}｜{r.get('组合操作')}")
    return "\n".join(lines)

with tabs[0]:
    st.text(daily_plan_text())

with tabs[1]:
    show(exe, ["code","name","V8动作","买入优先级","首次建仓","最大允许仓位","风险预算","建议持有天数","执行结论"])

with tabs[2]:
    show(pf, ["code","name","shares","cost","price","市值","浮盈浮亏","浮盈浮亏%","持仓建议","组合操作","V8综合分","买入优先级"])
    st.caption("持仓文件：data/portfolio/holdings.csv，可编辑 code,name,shares,cost")

with tabs[3]:
    show(wl, ["code","name","note","自选状态","V8动作","买入优先级","V8综合分","首次建仓","最大允许仓位","执行结论"])
    st.caption("新增股票请运行：scripts/start_v8_5_watchlist_center.command")

with tabs[4]:
    risk = pf.copy() if pf is not None and not pf.empty else pd.DataFrame()
    if not risk.empty and "持仓建议" in risk.columns:
        risk = risk[risk["持仓建议"].astype(str).str.contains("止损|减仓|回避", na=False)]
    show(risk)

with tabs[5]:
    st.json({
        "market": market,
        "portfolio": pf_summary,
        "watchlist": wl_summary,
        "services": snap.get("services", []),
        "configs": snap.get("configs", {}),
    })

if auto:
    time.sleep(sec)
    st.rerun()
