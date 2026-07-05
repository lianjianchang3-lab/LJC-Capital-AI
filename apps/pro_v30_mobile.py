import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.pro_v30.watchlist.watchlist_manager import WatchlistManager
from core.pro_v30.portfolio.holding_manager import HoldingManager
from core.pro_v30.dashboard.dashboard_v3 import DashboardV3

st.set_page_config(page_title="LJC Pro V3 Mobile", page_icon="📱", layout="centered")
st.title("📱 LJC Pro V3")
dash = DashboardV3()
watch = WatchlistManager()
hold = HoldingManager()

s = dash.summary()
c1,c2 = st.columns(2)
c1.metric("Alpha", s.get("alpha"))
c2.metric("仓位", s.get("position"))
st.success(s.get("summary"))

st.subheader("自选股作战")
wd = dash.watchlist_decision()
for _, x in wd.head(8).iterrows():
    line = f"{x.get('code')} {x.get('name')}｜{x.get('最终动作','观察')}｜Alpha {x.get('Alpha2.0','-')}｜{x.get('建议仓位','')}"
    if x.get("最终动作") == "买入关注":
        st.success(line)
    elif x.get("风险等级") == "高":
        st.error(line)
    else:
        st.info(line)

with st.expander("添加自选股"):
    code = st.text_input("代码")
    name = st.text_input("名称")
    group = st.text_input("分组", "未分组")
    if st.button("添加"):
        if code:
            watch.add(code, name, group, 1)
            st.success("已添加，请刷新")

with st.expander("我的持仓"):
    st.dataframe(dash.portfolio_decision(), use_container_width=True, hide_index=True)
