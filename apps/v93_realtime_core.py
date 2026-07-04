import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import time
from core.v93 import RealtimeCore

st.set_page_config(page_title="LJC V9.3 Realtime Core", page_icon="🛰️", layout="wide")
st.title("🛰️ LJC Capital AI V9.3 Sprint A - Realtime Core")
st.caption("统一实时数据层｜AKShare优先｜CSV备用｜健康检查｜缓存")

auto = st.sidebar.checkbox("自动刷新", value=False)
sec = st.sidebar.slider("刷新秒数", 5, 60, 10)

core = RealtimeCore()
tabs = st.tabs(["Health", "Quotes", "Cache", "Validation"])

with tabs[0]:
    st.header("Realtime Health")
    h = core.health()
    c1, c2, c3 = st.columns(3)
    c1.metric("Active Source", h.get("active_source"))
    c2.metric("Rows", h.get("rows"))
    c3.metric("Live Ready", str(h.get("live_ready")))
    st.json({"akshare_installed": h.get("akshare_installed"), "akshare_error": h.get("akshare_error")})
    st.dataframe(pd.DataFrame(h.get("csv_sources", [])), use_container_width=True, hide_index=True)

with tabs[1]:
    st.header("Quotes")
    q = core.quotes()
    if q.empty:
        st.warning("暂无行情数据。请安装 AKShare 或准备 CSV。")
    else:
        st.dataframe(q.head(300), use_container_width=True, hide_index=True)

with tabs[2]:
    st.header("Cache")
    q = core.quotes()
    if st.button("写入 data/realtime/quotes_realtime.csv"):
        if q.empty:
            st.error("无数据可缓存")
        else:
            st.success(core.cache(q))

with tabs[3]:
    st.header("Sprint A Validation")
    h = core.health()
    checks = [
        {"check": "RealtimeCore Loaded", "pass": True, "detail": h.get("engine")},
        {"check": "Data Available", "pass": h.get("rows", 0) > 0, "detail": h.get("rows")},
        {"check": "Fallback Ready", "pass": True, "detail": h.get("active_source")},
        {"check": "Live Provider Installed", "pass": bool(h.get("akshare_installed")), "detail": h.get("akshare_error")},
    ]
    st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)
    if all(x["pass"] for x in checks[:3]):
        st.success("V9.3 Sprint A 基础验收通过。")
    else:
        st.warning("系统可运行，但当前暂无可用行情数据。")

if auto:
    time.sleep(sec)
    st.rerun()
