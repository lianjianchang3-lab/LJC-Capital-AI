import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.pro_v40 import V40Commander, PositionController

st.set_page_config(page_title="LJC V4 Mobile", page_icon="📱", layout="centered")
st.title("📱 LJC V4 Commander")
d = V40Commander().dashboard()
s = d["state"]
c1,c2 = st.columns(2)
c1.metric("AI评分", s.get("ai_score"))
c2.metric("仓位", s.get("position"))
st.warning(f"市场：{s.get('state')}｜风险：{s.get('risk')}")
st.success(s.get("summary"))

st.subheader("今日三类信号")
for x in d.get("signals", [])[:8]:
    line = f"{x.get('机构信号')}｜{x.get('code')} {x.get('name')}｜AI {x.get('Unified AI Score')}"
    if "立即关注" in str(x.get("机构信号")):
        st.success(line)
    elif "禁止" in str(x.get("机构信号")):
        st.error(line)
    else:
        st.info(line)
    st.caption(x.get("证据链"))

with st.expander("仓位建议"):
    a = PositionController().allocation()
    st.write(a.get("summary"))
    st.dataframe(pd.DataFrame(a.get("items",[])), use_container_width=True, hide_index=True)
