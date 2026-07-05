import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.pro_v30.watchlist.watchlist_manager import WatchlistManager
from core.pro_v30.portfolio.holding_manager import HoldingManager
from core.pro_v30.dashboard.dashboard_v3 import DashboardV3

st.set_page_config(page_title="LJC Pro V3 Sprint3", page_icon="⚙️", layout="wide")
st.title("⚙️ LJC Capital AI Pro V3.0 Sprint 3")
st.caption("股票管理中心｜动态自选股｜持仓编辑｜AI驾驶舱")

auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N", 5, 100, 30)

watch = WatchlistManager()
hold = HoldingManager()
dash = DashboardV3()

tabs = st.tabs(["AI驾驶舱", "股票管理", "自选股作战", "持仓管理", "持仓决策", "手机部署"])

with tabs[0]:
    s = dash.summary()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Alpha", s.get("alpha"))
    c2.metric("风险", s.get("risk"))
    c3.metric("模式", s.get("mode"))
    c4.metric("仓位", s.get("position"))
    st.success(s.get("summary"))
    st.dataframe(pd.DataFrame(s.get("top",[])), use_container_width=True, hide_index=True)

with tabs[1]:
    st.subheader("添加/更新股票")
    c1,c2,c3,c4 = st.columns(4)
    code = c1.text_input("股票代码", "")
    name = c2.text_input("股票名称", "")
    group = c3.text_input("分组", "未分组")
    star = c4.selectbox("星标", [1,0], index=0)
    if st.button("添加/更新到自选股"):
        if code.strip():
            watch.add(code, name, group, star)
            st.success("已保存")
            st.rerun()

    st.subheader("当前自选股")
    df = watch.load()
    edited = st.data_editor(df, use_container_width=True, hide_index=True, num_rows="dynamic")
    if st.button("保存自选股表"):
        watch.save(edited)
        st.success("自选股已保存")
        st.rerun()

with tabs[2]:
    st.dataframe(dash.watchlist_decision().head(top), use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader("录入/更新持仓")
    c1,c2,c3,c4,c5 = st.columns(5)
    h_code = c1.text_input("持仓代码", "")
    h_name = c2.text_input("持仓名称", "")
    h_cost = c3.number_input("成本", min_value=0.0, value=0.0)
    h_shares = c4.number_input("股数", min_value=0.0, value=0.0)
    h_weight = c5.number_input("目标仓位", min_value=0.0, max_value=1.0, value=0.10)
    if st.button("添加/更新持仓"):
        if h_code.strip():
            hold.upsert(h_code, h_name, h_cost, h_shares, h_weight)
            st.success("持仓已保存")
            st.rerun()

    st.subheader("当前持仓")
    hdf = hold.load()
    edited_h = st.data_editor(hdf, use_container_width=True, hide_index=True, num_rows="dynamic")
    if st.button("保存持仓表"):
        hold.save(edited_h)
        st.success("持仓已保存")
        st.rerun()

with tabs[4]:
    st.dataframe(dash.portfolio_decision().head(top), use_container_width=True, hide_index=True)

with tabs[5]:
    st.code("python -m streamlit run apps/pro_v30_mobile.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
