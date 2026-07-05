import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from core.enterprise import EnterpriseCommander

st.set_page_config(page_title="LJC V7 Mobile", page_icon="📱", layout="centered")
st.title("📱 LJC V7 Commander")

snap = EnterpriseCommander().snapshot()
market = snap.get("market", {})

c1, c2 = st.columns(2)
c1.metric("市场", market.get("state"))
c2.metric("仓位", market.get("position"))
st.success(snap.get("summary"))

st.subheader("今日 LCRI Top")
for x in snap.get("lcri_top", [])[:8]:
    line = f"{x.get('Action','观察')}｜{x.get('code')} {x.get('name')}｜LCRI {x.get('LCRI Score')}｜仓位 {x.get('Position')}"
    if x.get("Action") == "A类关注":
        st.success(line)
    elif x.get("Action") == "C类回避":
        st.error(line)
    else:
        st.info(line)
    st.caption(x.get("Reason") or x.get("LCRI Evidence") or "")
