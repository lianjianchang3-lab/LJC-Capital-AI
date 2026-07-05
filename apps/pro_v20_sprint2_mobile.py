import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.pro_v20.commander import CommanderCenterV2
from core.pro_v20.tradeplan.trade_planner_v2 import TradePlannerV2
from core.pro_v20.alerts.alert_engine_v2 import AlertEngineV2

st.set_page_config(page_title="LJC Sprint2 Mobile", page_icon="📱", layout="centered")
st.title("📱 LJC AI总指挥")
d = CommanderCenterV2().dashboard()
c1,c2 = st.columns(2)
c1.metric("Alpha", d.get("alpha"))
c2.metric("仓位", d.get("position"))
st.warning(f"风险：{d.get('risk')}｜模式：{d.get('mode')}")
st.success(d.get("summary"))

st.subheader("今日作战")
for x in d.get("top", [])[:8]:
    line = f"{x.get('最终动作')}｜{x.get('code')} {x.get('name')}｜Alpha {x.get('Alpha2.0')}｜资金 {x.get('资金共振')}｜仓位 {x.get('建议仓位')}"
    if x.get("最终动作") == "买入关注":
        st.success(line)
    elif x.get("风险等级") == "高":
        st.error(line)
    else:
        st.info(line)
    st.caption(f"买入区间：{x.get('买入区间')}｜止损：{x.get('止损位')}｜目标：{x.get('第一目标')}/{x.get('第二目标')}｜{x.get('交易理由')}")

with st.expander("盘中预警"):
    st.dataframe(AlertEngineV2().scan(), use_container_width=True, hide_index=True)
