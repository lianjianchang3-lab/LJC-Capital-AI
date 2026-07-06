import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from core.cockpit import TradingCockpit
from core.watchlist_center import WatchlistCenter

st.set_page_config(page_title="LJC V8.5 Mobile", page_icon="📱", layout="centered")

snap = TradingCockpit().snapshot()
market = snap.get("market", {}) or {}

st.title("📱 LJC V8.5 Final")
c1, c2 = st.columns(2)
c1.metric("市场", market.get("state", "-"))
c2.metric("仓位", market.get("position", "-"))
st.success(snap.get("summary", "-"))

with st.expander("⭐ 加入自选股"):
    code = st.text_input("代码")
    name = st.text_input("名称")
    note = st.text_input("备注")
    if st.button("加入", use_container_width=True):
        if code:
            WatchlistCenter().add(code, name, note)
            st.success("已加入")
            st.rerun()

tab1, tab2, tab3 = st.tabs(["今天可以买", "风险", "自选"])

with tab1:
    buy = snap.get("buy")
    if buy is None or buy.empty:
        st.info("暂无强买入信号")
    else:
        for _, r in buy.head(8).iterrows():
            st.success(f"{r.get('code')} {r.get('name')}｜优先级{r.get('买入优先级')}｜首仓{r.get('首次建仓')}｜最大{r.get('最大允许仓位')}")
            st.caption(f"买点 {r.get('第一买点')}/{r.get('第二买点')}｜止损 {r.get('止损价')}｜目标 {r.get('第一止盈')}/{r.get('第二止盈')}")

with tab2:
    items = []
    for block in [snap.get("reduce"), snap.get("avoid")]:
        if block is not None and not block.empty:
            items += block.to_dict("records")
    if not items:
        st.info("暂无明显风险")
    for r in items[:8]:
        st.error(f"{r.get('code')} {r.get('name')}｜{r.get('持仓建议') or r.get('V8动作')}")
        st.caption(r.get("执行结论") or r.get("组合操作") or "")

with tab3:
    wl = snap.get("watchlist")
    if wl is None or wl.empty:
        st.info("暂无自选股")
    else:
        st.dataframe(wl, use_container_width=True, hide_index=True)
