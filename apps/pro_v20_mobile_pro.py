import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.pro_v20.decision import ProDecisionCenter
from core.pro_v20.trading import TradePlanEngine
from core.pro_v20.alerts import AlertCenter
from core.pro_v20.report import MorningReport

st.set_page_config(page_title="LJC Pro V2 手机Pro", page_icon="📱", layout="centered")
st.title("📱 LJC Pro V2.0")
st.caption("AI作战｜买卖点｜预警｜晨报")

brief = ProDecisionCenter().morning_brief()
c1,c2 = st.columns(2)
c1.metric("AI均分", brief.get("market_score"))
c2.metric("仓位", brief.get("position"))
st.success(brief.get("summary"))

st.subheader("今日交易计划")
plans = TradePlanEngine().plans()
for _, x in plans.head(10).iterrows():
    line = f"{x.get('红绿灯')} {x.get('交易动作')}｜{x.get('code')} {x.get('name')}｜Alpha {x.get('LJC Alpha Score')}｜仓位 {x.get('正式仓位')}"
    if x.get("红绿灯") == "🟢":
        st.success(line)
    elif x.get("红绿灯") == "🔴":
        st.error(line)
    else:
        st.info(line)
    st.caption(f"买点 {x.get('第一买点')}/{x.get('第二买点')}｜突破 {x.get('突破买点')}｜止损 {x.get('止损')}｜目标 {x.get('目标一')}/{x.get('目标二')}")

with st.expander("AI预警"):
    alerts = AlertCenter().generate()
    if alerts:
        for a in alerts[:10]:
            st.write(f"{a['level']}｜{a['code']} {a['name']}｜{a['alert']}｜{a['reason']}")
    else:
        st.write("暂无预警")

with st.expander("今日晨报"):
    st.markdown(MorningReport().generate_text())
