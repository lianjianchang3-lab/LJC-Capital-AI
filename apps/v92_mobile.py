import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.v92 import V92LiveDataEngine, V92LiveMonitor, V92RefreshCenter

st.set_page_config(page_title="LJC V9.2 Mobile", page_icon="📡", layout="centered")
st.title("📡 LJC V9.2 Mobile")
st.caption("实时行情｜实时扫描｜风险提示")

h = V92LiveDataEngine().health()
scan = V92LiveMonitor().scan()

c1, c2 = st.columns(2)
c1.metric("数据源", h.get("active_source"))
c2.metric("行数", h.get("rows"))
st.metric("实时接口", "ON" if h.get("live_ready") else "CSV备用")

if st.button("手动刷新实时缓存"):
    st.json(V92RefreshCenter().refresh_to_csv())

st.subheader("扫描结论")
st.success(scan.get("summary"))

items = scan.get("items", [])
if items:
    df = pd.DataFrame(items)
    for _, r in df.head(10).iterrows():
        sig = r.get("live_signal")
        text = f"{sig}｜{r.get('code')} {r.get('name')}｜Score {r.get('live_score')}｜Price {r.get('price')}"
        if sig == "BUY":
            st.success(text)
        elif sig == "RISK":
            st.error(text)
        else:
            st.info(text)
else:
    st.warning("暂无数据")
