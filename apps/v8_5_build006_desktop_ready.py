import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st
from core.mobile_ready import MobileCommander
from core.watchlist_center import WatchlistCenter

st.set_page_config(page_title="LJC V8.5 Build006", page_icon="🟢", layout="wide")
st.title("🟢 LJC V8.5 Build006｜开盘前稳定版")
st.caption("不等待 AkShare，全程可离线打开；数据源恢复后自动使用实时数据。")

@st.cache_data(ttl=10)
def load():
    snap = MobileCommander().snapshot()
    return snap

snap = load()
market = snap.get("market", {}) or {}

c1,c2,c3,c4 = st.columns(4)
c1.metric("市场", market.get("state","-"))
c2.metric("建议仓位", market.get("position","-"))
c3.metric("机会", len(snap.get("buy", [])))
c4.metric("风险", len(snap.get("risk", [])))
st.success(snap.get("summary","-"))

tabs = st.tabs(["今天可以买", "自选股", "风险", "数据源状态"])

def show(df):
    if df is None or df.empty:
        st.warning("暂无数据")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

with tabs[0]:
    show(snap.get("buy"))

with tabs[1]:
    with st.form("add_watch"):
        a,b,c = st.columns(3)
        code = a.text_input("代码")
        name = b.text_input("名称")
        note = c.text_input("备注")
        ok = st.form_submit_button("加入自选")
        if ok and code:
            WatchlistCenter().add(code, name, note)
            st.success("已加入自选")
            st.cache_data.clear()
    show(snap.get("watchlist"))

with tabs[2]:
    show(snap.get("risk"))

with tabs[3]:
    st.json(snap.get("status", {}))
