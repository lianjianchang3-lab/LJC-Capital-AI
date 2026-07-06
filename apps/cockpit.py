import pandas as pd
import streamlit as st
from core.cockpit import TradingCockpit
from core.watchlist_center import WatchlistCenter

def _records(x):
    if isinstance(x, pd.DataFrame):
        return x.to_dict("records")
    try:
        return pd.DataFrame(x or []).to_dict("records")
    except Exception:
        return []

def render_cockpit():
    st.title("🛫 LJC Capital AI Pro V8.5 Final")
    st.caption("交易驾驶舱｜自选股｜持仓｜每日计划｜手机同步")

    with st.sidebar.expander("⭐ 快速加入自选股", expanded=True):
        code = st.text_input("代码", placeholder="300059")
        name = st.text_input("名称", placeholder="东方财富")
        note = st.text_input("备注", placeholder="核心观察")
        if st.button("加入自选", use_container_width=True) and code.strip():
            WatchlistCenter().add(code, name, note)
            st.success("已加入自选股")
            st.rerun()

    @st.cache_data(ttl=10)
    def load():
        snap = TradingCockpit().snapshot()
        for k in ["execution","portfolio","watchlist","buy","hold","reduce","avoid"]:
            snap[k] = _records(snap.get(k))
        return snap

    snap = load()
    market = snap.get("market", {}) or {}
    pf_summary = snap.get("portfolio_summary", {}) or {}
    wl_summary = snap.get("watchlist_summary", {}) or {}
    health = snap.get("radar_health", {}) or {}

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("市场", market.get("state","-"))
    c2.metric("建议仓位", market.get("position","-"))
    c3.metric("LCRI均分", market.get("lcri_avg","-"))
    c4.metric("扫描数", health.get("lcri_count",0))
    c5.metric("持仓市值", pf_summary.get("total_value","-"))
    c6.metric("自选重点", wl_summary.get("focus","-"))

    st.success(snap.get("summary","-"))
    st.info((pf_summary.get("summary","-")) + "｜" + (wl_summary.get("summary","-")))

    tabs = st.tabs(["总控计划","今天可以买","我的持仓","自选股","全部信号","风险/回避","系统"])

    def show(data, cols=None):
        d = pd.DataFrame(data or [])
        if d.empty:
            st.warning("暂无数据")
            return
        if cols:
            use = [c for c in cols if c in d.columns]
            if use:
                d = d[use]
        st.dataframe(d, use_container_width=True, hide_index=True)

    with tabs[0]:
        st.text(snap.get("plan_text","暂无计划"))
    with tabs[1]:
        show(snap.get("buy"), ["code","name","V8动作","买入优先级","V8综合分","首次建仓","最大允许仓位","风险预算","第一买点","第二买点","止损价","第一止盈","第二止盈","执行结论"])
    with tabs[2]:
        show(snap.get("portfolio"), ["code","name","shares","cost","price","市值","浮盈浮亏","浮盈浮亏%","持仓建议","组合操作","V8综合分","买入优先级"])
        st.caption("持仓文件：data/portfolio/holdings.csv，可编辑 code,name,shares,cost")
    with tabs[3]:
        show(snap.get("watchlist"), ["code","name","note","自选状态","V8动作","买入优先级","V8综合分","首次建仓","最大允许仓位","执行结论"])
    with tabs[4]:
        show(snap.get("execution"))
    with tabs[5]:
        st.subheader("持仓风险")
        show(snap.get("reduce"))
        st.subheader("信号回避")
        show(snap.get("avoid"))
    with tabs[6]:
        st.json({"version":"8.5.0-final","market":market,"radar_health":health,"portfolio_summary":pf_summary,"watchlist_summary":wl_summary})
