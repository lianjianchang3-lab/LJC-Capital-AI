import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.v91 import V91RealtimeHub, V91AutoScanner, V91SignalCenter

st.set_page_config(page_title="LJC V9.1 Mobile", page_icon="📱", layout="centered")
st.title("📱 LJC V9.1 Mobile")
st.caption("实时扫描｜买卖信号｜风险提示")

h = V91RealtimeHub().health()
scan = V91AutoScanner().scan()
sig = V91SignalCenter().generate()

st.subheader("今日状态")
c1, c2 = st.columns(2)
c1.metric("数据源", h.get("active_source"))
c2.metric("行数", h.get("rows"))

st.subheader("扫描结论")
st.success(scan.get("summary"))

signals = sig.get("signals", [])
st.subheader("实时信号")
if signals:
    for s in signals:
        if s["signal"] == "BUY":
            st.success(f"BUY｜{s['code']} {s['name']}｜Score {s['score']}")
        elif s["signal"] == "RISK_ALERT":
            st.error(f"RISK｜{s['code']} {s['name']}｜Score {s['score']}")
        else:
            st.warning(f"{s['signal']}｜{s['code']} {s['name']}｜Score {s['score']}")
        st.caption(s.get("reason"))
else:
    st.info("暂无强信号。")

with st.expander("全部扫描结果"):
    st.dataframe(pd.DataFrame(scan.get("items", [])), use_container_width=True, hide_index=True)
