import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from core.enterprise import EnterpriseCommander

st.set_page_config(page_title="LJC V7.1 Mobile Pro", page_icon="📱", layout="centered")

snap = EnterpriseCommander().snapshot()
market = snap.get("market", {}) or {}
health = snap.get("radar_health", {}) or {}

st.title("📱 LJC V7.1 Pro")
c1, c2 = st.columns(2)
c1.metric("市场", market.get("state", "-"))
c2.metric("仓位", market.get("position", "-"))
st.success(snap.get("summary", "-"))

st.subheader("今日行动")
top = snap.get("trader_top") or snap.get("lcri_top") or []
for x in top[:10]:
    action = x.get("执行建议") or x.get("Action") or "观察"
    code = x.get("code", "")
    name = x.get("name", "")
    score = x.get("AI交易强度") or x.get("LCRI Score") or "-"
    pos = x.get("建议仓位V5") or x.get("Position") or "-"
    text = f"{action}｜{code} {name}｜分数 {score}｜仓位 {pos}"
    if "买入" in str(action) or "A类" in str(action):
        st.success(text)
    elif "回避" in str(action) or "减仓" in str(action):
        st.error(text)
    else:
        st.info(text)
    st.caption(
        f"买点 {x.get('第一买点','-')}/{x.get('第二买点','-')}｜"
        f"止损 {x.get('止损价','-')}｜"
        f"LCRI {x.get('LCRI Score','-')}"
    )
