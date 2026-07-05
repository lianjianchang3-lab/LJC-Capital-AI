import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from core.enterprise import EnterpriseCommander
from core.professional import LCRIPro, InstitutionCenter

st.set_page_config(page_title="LJC V8 Mobile", page_icon="📱", layout="centered")
snap = EnterpriseCommander().snapshot()
market = snap.get("market", {}) or {}
inst_sum = InstitutionCenter().summary()
df = LCRIPro().dataframe()

st.title("📱 LJC V8 Pro")
c1,c2 = st.columns(2)
c1.metric("市场", market.get("state","-"))
c2.metric("仓位", market.get("position","-"))
st.success(snap.get("summary","-"))
st.info(inst_sum.get("summary","-"))

st.subheader("今日执行")
for _, r in df.head(10).iterrows():
    text = f"{r.get('V8动作')}｜{r.get('code')} {r.get('name')}｜综合{r.get('V8综合分')}｜胜率{r.get('胜率估算')}%｜仓位{r.get('V8仓位')}"
    if r.get("V8动作") == "强势关注":
        st.success(text)
    elif r.get("V8动作") == "回避":
        st.error(text)
    else:
        st.info(text)
    st.caption(f"买点 {r.get('第一买点')}/{r.get('第二买点')}｜止损 {r.get('止损价')}｜目标 {r.get('第一止盈')}/{r.get('第二止盈')}")
