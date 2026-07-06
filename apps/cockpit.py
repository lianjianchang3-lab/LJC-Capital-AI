import pandas as pd
import streamlit as st

from core.cockpit import TradingCockpit
from core.watchlist_center import WatchlistCenter


def _to_records(x):
    if isinstance(x, pd.DataFrame):
        return x.to_dict("records")
    try:
        return pd.DataFrame(x or []).to_dict("records")
    except Exception:
        return []


def render_cockpit():
    st.title("🛫 LJC Capital AI Pro V8.5 Final")
    st.caption("统一交易驾驶舱｜自选股｜持仓｜执行中心｜风险｜手机同步")

    with st.sidebar:
        st.subheader("启动入口")
        st.code("scripts/start_desktop.command\nscripts/start_mobile.command")
        st.markdown("---")
        st.subheader("⭐ 加入自选股")
        code = st.text_input("股票代码", placeholder="300059")
        name = st.text_input("股票名称", placeholder="东方财富")
        note = st.text_input("备注", placeholder="核心观察")
        if st.button("加入自选", use_container_width=True):
            if code.strip():
                WatchlistCenter().add(code, name, note)
                st.success("已加入自选股")
                st.cache_data.clear()
                st.rerun()
            else:
                st.warning("请输入股票代码")

    @st.cache_data(ttl=10)
    def load_snapshot():
        snap = TradingCockpit().snapshot()
        for key in ["execution", "portfolio", "watchlist", "buy", "hold", "reduce", "avoid"]:
            snap[key] = _to_records(snap.get(key))
        return snap

    try:
        snap = load_snapshot()
    except Exception as e:
        st.error(f"驾驶舱加载失败：{e}")
        st.stop()

    market = snap.get("market", {}) or {}
    pf_summary = snap.get("portfolio_summary", {}) or {}
    wl_summary = snap.get("watchlist_summary", {}) or {}
    health = snap.get("radar_health", {}) or {}

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("市场", market.get("state", "-"))
    c2.metric("建议仓位", market.get("position", "-"))
    c3.metric("LCRI均分", market.get("lcri_avg", "-"))
    c4.metric("扫描数", health.get("lcri_count", 0))
    c5.metric("持仓市值", pf_summary.get("total_value", "-"))
    c6.metric("自选重点", wl_summary.get("focus", "-"))

    st.success(snap.get("summary", "-"))
    st.info((pf_summary.get("summary", "-")) + "｜" + (wl_summary.get("summary", "-")))

    tabs = st.tabs(["总控计划", "今天可以买", "我的持仓", "自选股", "全部执行信号", "风险/回避", "系统状态"])

    def show(data, cols=None):
        df = pd.DataFrame(data or [])
        if df.empty:
            st.warning("暂无数据")
            return
        if cols:
            use = [c for c in cols if c in df.columns]
            if use:
                df = df[use]
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tabs[0]:
        st.text(snap.get("plan_text", "暂无计划"))

    with tabs[1]:
        show(snap.get("buy"), [
            "code","name","V8动作","买入优先级","V8综合分","首次建仓","最大允许仓位",
            "风险预算","第一买点","第二买点","突破确认价","止损价","第一止盈","第二止盈","执行结论"
        ])

    with tabs[2]:
        show(snap.get("portfolio"), [
            "code","name","shares","cost","price","市值","浮盈浮亏","浮盈浮亏%",
            "持仓建议","组合操作","V8综合分","买入优先级"
        ])
        st.caption("持仓文件：data/portfolio/holdings.csv，列：code,name,shares,cost")

    with tabs[3]:
        show(snap.get("watchlist"), [
            "code","name","note","自选状态","V8动作","买入优先级","V8综合分",
            "首次建仓","最大允许仓位","执行结论"
        ])
        st.caption("自选股文件：data/watchlist/watchlist.csv，列：code,name,note")

    with tabs[4]:
        show(snap.get("execution"))

    with tabs[5]:
        st.subheader("持仓风险")
        show(snap.get("reduce"))
        st.subheader("信号回避")
        show(snap.get("avoid"))

    with tabs[6]:
        st.json({
            "version": "8.5.0-final",
            "market": market,
            "radar_health": health,
            "portfolio_summary": pf_summary,
            "watchlist_summary": wl_summary,
            "archive": "_archive/",
        })
