import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.v93 import RealtimeCore, V93MarketScanner, V93SignalEngine

st.set_page_config(page_title="LJC V9.3 Mobile Scanner", page_icon="📱", layout="centered")
st.title("📱 LJC V9.3 Mobile Scanner")
st.caption("实时源｜AI评分V3｜买卖信号")

h = RealtimeCore().health()
scan = V93MarketScanner().scan(top_n=30)
sig = V93SignalEngine().generate()

c1, c2 = st.columns(2)
c1.metric("数据源", h.get("active_source"))
c2.metric("行数", h.get("rows"))
st.metric("实时", "ON" if h.get("live_ready") else "CSV备用")

st.subheader("扫描结论")
st.success(scan.get("summary"))

st.subheader("信号")
signals = sig.get("signals", [])
if signals:
    for s in signals[:20]:
        text = f"{s.get('decision')}｜{s.get('code')} {s.get('name')}｜AI {s.get('ai_score_v3')}｜仓位 {s.get('position')}"
        if s.get("decision") == "BUY":
            st.success(text)
        elif s.get("decision") == "RISK_ALERT":
            st.error(text)
        else:
            st.info(text)
        st.caption(s.get("reason"))
else:
    st.info("暂无强信号")

with st.expander("Top扫描结果"):
    st.dataframe(pd.DataFrame(scan.get("items", [])), use_container_width=True, hide_index=True)
