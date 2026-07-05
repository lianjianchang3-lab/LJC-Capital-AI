import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.build006 import Build006Commander

st.set_page_config(page_title="LJC Build006 Mobile", page_icon="📱", layout="centered")
st.title("📱 LJC AI Pro Build 006")
st.caption("今日策略｜买入关注｜主升浪｜交易计划")

cmd = Build006Commander()
d = cmd.dashboard()

c1,c2 = st.columns(2)
c1.metric("AI评分", d.get("market_score"))
c2.metric("仓位", d.get("position"))
st.warning(f"风险：{d.get('risk')}")
st.success(d.get("summary"))

st.subheader("今日重点")
for x in d.get("top", [])[:10]:
    text = f"{x.get('星级')}｜{x.get('操作建议')}｜{x.get('code')} {x.get('name')}｜评分 {x.get('LJC评分')}｜仓位 {x.get('建议仓位')}"
    if x.get("操作建议") == "买入关注":
        st.success(text)
    elif x.get("操作建议") == "减仓/回避":
        st.error(text)
    else:
        st.info(text)
    st.caption(f"阶段：{x.get('主升浪阶段')}｜现价：{x.get('price')}｜止损：{x.get('止损参考')}｜目标：{x.get('目标一')}/{x.get('目标二')}")

with st.expander("交易计划"):
    st.dataframe(pd.DataFrame(cmd.trading_plan().get("plans",[])), use_container_width=True, hide_index=True)
