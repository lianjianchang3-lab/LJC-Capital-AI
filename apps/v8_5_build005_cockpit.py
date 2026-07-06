import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st
from core.cockpit import TradingCockpit
from core.watchlist_center import WatchlistCenter

st.set_page_config(page_title="LJC V8.5 Trading Cockpit", page_icon="🛫", layout="wide")
st.title("🛫 LJC Capital AI Pro V8.5 Build005｜交易驾驶舱")
st.caption("市场总控｜AI执行｜我的持仓｜自选股｜每日交易计划")

auto = st.sidebar.checkbox("自动刷新", False)
sec = st.sidebar.slider("刷新秒数", 15, 180, 60)
top = st.sidebar.slider("显示前N", 5, 100, 30)

with st.sidebar.expander("⭐ 快速加入自选股", expanded=True):
    code = st.text_input("代码", placeholder="300059")
    name = st.text_input("名称", placeholder="东方财富")
    note = st.text_input("备注", placeholder="核心观察")
    if st.button("加入自选", use_container_width=True):
        if code.strip():
            WatchlistCenter().add(code, name, note)
            st.success("已加入自选股")
            st.rerun()

@st.cache_data(ttl=8)
def load_snapshot():
    snap = TradingCockpit().snapshot()
    # DataFrame cannot always serialize safely through cache if object types exist.
    # Return records for UI stability.
    return {
        **snap,
        "execution": snap["execution"].to_dict("records") if isinstance(snap.get("execution"), pd.DataFrame) else [],
        "portfolio": snap["portfolio"].to_dict("records") if isinstance(snap.get("portfolio"), pd.DataFrame) else [],
        "watchlist": snap["watchlist"].to_dict("records") if isinstance(snap.get("watchlist"), pd.DataFrame) else [],
        "buy": snap["buy"].to_dict("records") if isinstance(snap.get("buy"), pd.DataFrame) else [],
        "hold": snap["hold"].to_dict("records") if isinstance(snap.get("hold"), pd.DataFrame) else [],
        "reduce": snap["reduce"].to_dict("records") if isinstance(snap.get("reduce"), pd.DataFrame) else [],
        "avoid": snap["avoid"].to_dict("records") if isinstance(snap.get("avoid"), pd.DataFrame) else [],
    }

snap = load_snapshot()
market = snap.get("market", {}) or {}
pf_summary = snap.get("portfolio_summary", {}) or {}
wl_summary = snap.get("watchlist_summary", {}) or {}
health = snap.get("radar_health", {}) or {}

c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("市场", market.get("state","-"))
c2.metric("建议仓位", market.get("position","-"))
c3.metric("LCRI均分", market.get("lcri_avg","-"))
c4.metric("扫描数", health.get("lcri_count", 0))
c5.metric("持仓市值", pf_summary.get("total_value","-"))
c6.metric("自选重点", wl_summary.get("focus","-"))

st.success(snap.get("summary", "-"))
st.info((pf_summary.get("summary","-")) + "｜" + (wl_summary.get("summary","-")))

tabs = st.tabs(["总控计划", "今天可以买", "我的持仓", "自选股", "全部执行信号", "风险/回避", "系统"])

def df(key):
    return pd.DataFrame(snap.get(key, []) or [])

def show(data, cols=None):
    d = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data or [])
    if d.empty:
        st.warning("暂无数据")
        return
    if cols:
        use = [c for c in cols if c in d.columns]
        if use:
            d = d[use]
    st.dataframe(d.head(top), use_container_width=True, hide_index=True)

with tabs[0]:
    st.text(snap.get("plan_text", "暂无计划"))

with tabs[1]:
    show(df("buy"), ["code","name","V8动作","买入优先级","V8综合分","首次建仓","最大允许仓位","风险预算","第一买点","第二买点","突破确认价","止损价","第一止盈","第二止盈","执行结论"])

with tabs[2]:
    show(df("portfolio"), ["code","name","shares","cost","price","市值","浮盈浮亏","浮盈浮亏%","持仓建议","组合操作","V8综合分","买入优先级"])

with tabs[3]:
    show(df("watchlist"), ["code","name","note","自选状态","V8动作","买入优先级","V8综合分","首次建仓","最大允许仓位","执行结论"])
    st.caption("也可单独启动：scripts/start_v8_5_watchlist_center.command")

with tabs[4]:
    show(df("execution"), ["code","name","V8动作","买入优先级","V8综合分","首次建仓","最大允许仓位","风险预算","建议持有天数","执行结论"])

with tabs[5]:
    st.subheader("持仓风险")
    show(df("reduce"))
    st.subheader("信号回避")
    show(df("avoid"))

with tabs[6]:
    st.json({
        "market": market,
        "radar_health": health,
        "portfolio_summary": pf_summary,
        "watchlist_summary": wl_summary,
        "services": snap.get("services", []),
    })

if auto:
    time.sleep(sec)
    st.rerun()
