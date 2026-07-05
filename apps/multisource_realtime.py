import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.multisource import MultiSourceRealtimeHub

st.set_page_config(page_title="LJC 多源实时", page_icon="🟢", layout="wide")
st.title("🟢 LJC 多源实时数据系统")
st.caption("AKShare失败自动切新浪/腾讯/CSV｜确保周一可用")

hub = MultiSourceRealtimeHub()
st.sidebar.header("控制")
auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N", 8, 300, 80)

tabs = st.tabs(["总控台", "实时数据", "AI评分", "健康检查", "周一方案", "手机部署"])

with tabs[0]:
    h = hub.health()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("当前数据源", h["active_source"])
    c2.metric("行数", h["rows"])
    c3.metric("全市场", "OK" if h["full_market_ready"] else "备用")
    c4.metric("重点股", "OK" if h["watchlist_ready"] else "等待")
    if h["rows"] > 0:
        st.success("系统可用：若AKShare失败，将自动使用新浪/腾讯重点股实时或CSV缓存。")
    else:
        st.error("所有数据源均失败，需要检查网络。")

with tabs[1]:
    df = hub.quotes()
    st.dataframe(df.head(top), use_container_width=True, hide_index=True)

with tabs[2]:
    s = hub.score()
    if s.empty:
        st.warning("暂无评分数据")
    else:
        st.dataframe(s.head(top), use_container_width=True, hide_index=True)

with tabs[3]:
    st.json(hub.health())

with tabs[4]:
    st.markdown("""
## 周一保障策略

1. 优先尝试 AKShare 东方财富全市场。
2. 如果东方财富断开，自动切换新浪重点股实时。
3. 如果新浪失败，自动切换腾讯重点股实时。
4. 如果全部实时源失败，读取本地 CSV 缓存。
5. 周一至少保证你的重点观察池可以跑起来。
""")

with tabs[5]:
    st.code("python -m streamlit run apps/multisource_mobile.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
