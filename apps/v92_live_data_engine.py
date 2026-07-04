import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import time

from core.v92 import V92LiveDataEngine, V92RefreshCenter, V92LiveMonitor

st.set_page_config(page_title="LJC V9.2 Live Data Engine", page_icon="📡", layout="wide")
st.title("📡 LJC Capital AI V9.2 Live Data Engine")
st.caption("真实行情接口框架｜AKShare适配｜实时CSV缓存｜实时扫描增强")

auto = st.sidebar.checkbox("自动刷新", value=False)
sec = st.sidebar.slider("刷新秒数", 3, 60, 10)

tabs = st.tabs(["Live Data", "Refresh Center", "Live Monitor", "Validation", "Mobile Deploy"])

with tabs[0]:
    st.header("Live Data Engine")
    engine = V92LiveDataEngine()
    h = engine.health()
    a,b,c = st.columns(3)
    a.metric("Active Source", h.get("active_source"))
    b.metric("Rows", h.get("rows"))
    c.metric("Live Ready", str(h.get("live_ready")))
    st.json({"akshare_installed": h.get("akshare_installed"), "akshare_error": h.get("akshare_error")})
    st.dataframe(pd.DataFrame(h.get("csv_sources", [])), use_container_width=True, hide_index=True)
    q = engine.get_quotes(prefer_live=True)
    if not q.empty:
        st.subheader("Quotes Preview")
        st.dataframe(q.head(200), use_container_width=True, hide_index=True)

with tabs[1]:
    st.header("Refresh Center")
    if st.button("刷新并写入 data/realtime/quotes_realtime.csv"):
        st.json(V92RefreshCenter().refresh_to_csv())
    st.info("如果 AKShare 可用，将自动把实时行情写入 realtime CSV；否则继续使用本地CSV备用。")

with tabs[2]:
    st.header("Live Monitor")
    scan = V92LiveMonitor().scan()
    st.success(scan.get("summary"))
    st.dataframe(pd.DataFrame(scan.get("items", [])), use_container_width=True, hide_index=True)

with tabs[3]:
    st.header("V9.2 Validation")
    h = V92LiveDataEngine().health()
    checks = [
        {"check": "Live Engine Loaded", "pass": True, "detail": h.get("engine")},
        {"check": "Data Available", "pass": h.get("rows", 0) > 0, "detail": h.get("rows")},
        {"check": "AKShare Installed", "pass": bool(h.get("akshare_installed")), "detail": h.get("akshare_error")},
        {"check": "Live Monitor Running", "pass": V92LiveMonitor().scan().get("status") in ["OK","NO DATA"], "detail": "ok"},
    ]
    st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)
    if all(x["pass"] for x in checks):
        st.success("V9.2 Live Data Engine 验收通过，实时接口可用。")
    else:
        st.warning("V9.2 可运行；如 AKShare 未安装或不可用，将自动使用 CSV 备用。")

with tabs[4]:
    st.header("Mobile Deploy")
    st.code("python -m streamlit run apps/v92_mobile.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
