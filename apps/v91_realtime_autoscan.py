import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import time
from core.v91 import V91RealtimeHub, V91AutoScanner, V91SignalCenter

st.set_page_config(page_title="LJC V9.1 Realtime AutoScan", page_icon="⚡", layout="wide")
st.title("⚡ LJC Capital AI V9.1 Realtime AutoScan")
st.caption("实时行情｜自动扫描｜信号中心｜手机提醒基础版")

refresh = st.sidebar.slider("刷新秒数", 3, 60, 10)
auto_refresh = st.sidebar.checkbox("自动刷新", value=False)

tabs = st.tabs(["Realtime Hub", "Auto Scanner", "Signal Center", "Validation"])

with tabs[0]:
    st.header("Realtime Hub")
    h = V91RealtimeHub().health()
    a,b,c = st.columns(3)
    a.metric("Active Source", h.get("active_source"))
    b.metric("Rows", h.get("rows"))
    c.metric("Realtime", str(h.get("realtime")))
    st.dataframe(pd.DataFrame(h.get("sources", [])), use_container_width=True, hide_index=True)
    q = V91RealtimeHub().quotes()
    if not q.empty:
        st.subheader("Quotes")
        st.dataframe(q, use_container_width=True, hide_index=True)

with tabs[1]:
    st.header("Auto Scanner")
    scan = V91AutoScanner().scan()
    st.success(scan.get("summary"))
    st.dataframe(pd.DataFrame(scan.get("items", [])), use_container_width=True, hide_index=True)

with tabs[2]:
    st.header("Signal Center")
    sig = V91SignalCenter().generate()
    st.info(sig.get("summary"))
    st.dataframe(pd.DataFrame(sig.get("signals", [])), use_container_width=True, hide_index=True)

with tabs[3]:
    st.header("V9.1 Validation")
    h = V91RealtimeHub().health()
    scan = V91AutoScanner().scan()
    checks = [
        {"check":"Realtime Hub Loaded", "pass": True},
        {"check":"Data Available", "pass": h.get("rows", 0) > 0},
        {"check":"Scanner Running", "pass": scan.get("status") in ["OK","NO DATA"]},
        {"check":"Signal Center Running", "pass": "signals" in V91SignalCenter().generate()},
    ]
    st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)
    if all(x["pass"] for x in checks):
        st.success("V9.1 实时扫描基础版验收通过。")
    else:
        st.warning("系统可运行，但实时数据文件尚未准备。")

if auto_refresh:
    time.sleep(refresh)
    st.rerun()
