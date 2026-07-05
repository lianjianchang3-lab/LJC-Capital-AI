import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.pro_v30 import PortfolioCenterV3, MorningBriefPro
from core.pro_v20.commander import CommanderCenterV2

st.set_page_config(page_title="LJC Pro V3 Mobile", page_icon="📱", layout="centered")
st.title("📱 LJC Pro V3")
d = CommanderCenterV2().dashboard()
c1,c2 = st.columns(2)
c1.metric("Alpha", d.get("alpha"))
c2.metric("仓位", d.get("position"))
st.warning(f"风险 {d.get('risk')}｜模式 {d.get('mode')}")
st.success(d.get("summary"))

st.subheader("今日重点")
for x in d.get("top", [])[:8]:
    line = f"{x.get('最终动作')}｜{x.get('code')} {x.get('name')}｜Alpha {x.get('Alpha2.0')}｜仓位 {x.get('建议仓位')}"
    if x.get("最终动作") == "买入关注":
        st.success(line)
    elif x.get("风险等级") == "高":
        st.error(line)
    else:
        st.info(line)

with st.expander("我的持仓"):
    p = PortfolioCenterV3().analyze()
    st.write(p.get("summary"))
    st.dataframe(p.get("table"), use_container_width=True, hide_index=True)

with st.expander("晨会Pro"):
    st.text(MorningBriefPro().text())
