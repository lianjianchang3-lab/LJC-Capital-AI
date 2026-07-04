import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import time

from core.v93 import RealtimeCore, V93MarketScanner, V93SignalEngine

st.set_page_config(page_title="LJC V9.3 Sprint B Scanner", page_icon="⚡", layout="wide")
st.title("⚡ LJC Capital AI V9.3 Sprint B - AutoSwitch Scanner")
st.caption("AKShare自动切换｜实时扫描｜AI评分V3｜信号中心｜手机同步")

auto = st.sidebar.checkbox("自动刷新", value=False)
sec = st.sidebar.slider("刷新秒数", 5, 60, 10)
top_n = st.sidebar.slider("显示Top N", 10, 200, 50)

tabs = st.tabs(["Realtime Health", "Market Scanner", "AI Signals", "Validation", "Mobile Deploy"])

with tabs[0]:
    st.header("Realtime Health")
    h = RealtimeCore().health()
    c1, c2, c3 = st.columns(3)
    c1.metric("Active Source", h.get("active_source"))
    c2.metric("Rows", h.get("rows"))
    c3.metric("Live Ready", str(h.get("live_ready")))
    st.json({"akshare_installed": h.get("akshare_installed"), "akshare_error": h.get("akshare_error")})
    st.dataframe(pd.DataFrame(h.get("csv_sources", [])), use_container_width=True, hide_index=True)

with tabs[1]:
    st.header("Market Scanner")
    scan = V93MarketScanner().scan(top_n=top_n)
    st.success(scan.get("summary"))
    st.json({"source": scan.get("source"), "rows": scan.get("rows"), "buy_count": scan.get("buy_count"), "watch_buy_count": scan.get("watch_buy_count"), "risk_count": scan.get("risk_count")})
    st.dataframe(pd.DataFrame(scan.get("items", [])), use_container_width=True, hide_index=True)

with tabs[2]:
    st.header("AI Signals")
    sig = V93SignalEngine().generate()
    st.info(sig.get("summary"))
    st.dataframe(pd.DataFrame(sig.get("signals", [])), use_container_width=True, hide_index=True)

with tabs[3]:
    st.header("Sprint B Validation")
    h = RealtimeCore().health()
    scan = V93MarketScanner().scan(top_n=20)
    sig = V93SignalEngine().generate()
    checks = [
        {"check": "RealtimeCore Running", "pass": True, "detail": h.get("active_source")},
        {"check": "Data Available", "pass": h.get("rows", 0) > 0, "detail": h.get("rows")},
        {"check": "Scanner Running", "pass": scan.get("status") == "OK", "detail": scan.get("summary")},
        {"check": "Signal Engine Running", "pass": "signals" in sig, "detail": len(sig.get("signals", []))},
    ]
    st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)
    if all(x["pass"] for x in checks):
        st.success("V9.3 Sprint B 验收通过。")
    else:
        st.warning("Sprint B 可运行，但行情数据或实时源仍需检查。")

with tabs[4]:
    st.header("Mobile Deploy")
    st.code("python -m streamlit run apps/v93_mobile_scanner.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
