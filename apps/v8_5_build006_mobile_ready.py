import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st
from core.mobile_ready import MobileCommander
from core.watchlist_center import WatchlistCenter

st.set_page_config(page_title="LJC V8.5 Mobile Ready", page_icon="📱", layout="centered")

st.title("📱 LJC V8.5 开盘前手机版")
st.caption("Build006：离线缓存｜不等 AkShare｜手机稳定打开")

@st.cache_data(ttl=10)
def load():
    snap = MobileCommander().snapshot()
    return {
        **snap,
        "execution": snap["execution"].to_dict("records") if isinstance(snap.get("execution"), pd.DataFrame) else [],
        "watchlist": snap["watchlist"].to_dict("records") if isinstance(snap.get("watchlist"), pd.DataFrame) else [],
        "portfolio": snap["portfolio"].to_dict("records") if isinstance(snap.get("portfolio"), pd.DataFrame) else [],
        "buy": snap["buy"].to_dict("records") if isinstance(snap.get("buy"), pd.DataFrame) else [],
        "risk": snap["risk"].to_dict("records") if isinstance(snap.get("risk"), pd.DataFrame) else [],
    }

snap = load()
market = snap.get("market", {}) or {}

c1, c2 = st.columns(2)
c1.metric("市场", market.get("state", "-"))
c2.metric("仓位", market.get("position", "-"))
st.success(snap.get("summary", "-"))

with st.expander("⭐ 快速加入自选股"):
    code = st.text_input("代码", placeholder="300059")
    name = st.text_input("名称", placeholder="东方财富")
    note = st.text_input("备注", placeholder="核心观察")
    if st.button("加入自选", use_container_width=True):
        if code.strip():
            WatchlistCenter().add(code, name, note)
            st.success("已加入")
            st.cache_data.clear()
            st.rerun()

tab1, tab2, tab3, tab4 = st.tabs(["今天可以买", "风险", "自选股", "状态"])

with tab1:
    buy = snap.get("buy", [])
    if not buy:
        st.info("暂无强买入信号，先观察。")
    for r in buy[:10]:
        st.success(f"{r.get('code')} {r.get('name')}｜优先级{r.get('买入优先级')}｜首仓{r.get('首次建仓')}｜最大{r.get('最大允许仓位')}")
        st.caption(f"买点 {r.get('第一买点','-')}/{r.get('第二买点','-')}｜止损 {r.get('止损价','-')}｜目标 {r.get('第一止盈','-')}/{r.get('第二止盈','-')}")

with tab2:
    risk = snap.get("risk", [])
    if not risk:
        st.info("暂无明显风险")
    for r in risk[:10]:
        st.error(f"{r.get('code')} {r.get('name')}｜{r.get('持仓建议') or r.get('V8动作') or '风险'}")
        st.caption(r.get("执行结论") or r.get("组合操作") or "")

with tab3:
    wl = pd.DataFrame(snap.get("watchlist", []))
    if wl.empty:
        st.warning("暂无自选股")
    else:
        cols = [c for c in ["code","name","note","自选状态","买入优先级","V8综合分","执行结论"] if c in wl.columns]
        st.dataframe(wl[cols] if cols else wl, use_container_width=True, hide_index=True)

with tab4:
    st.json(snap.get("status", {}))
