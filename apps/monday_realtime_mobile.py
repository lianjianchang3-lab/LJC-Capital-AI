import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.monday_realtime import MondayRealtimeSystem

st.set_page_config(page_title="LJC 周一手机端", page_icon="📱", layout="centered")
st.title("📱 LJC 周一实时终端")
st.caption("实时行情｜AI评分｜买入关注｜风险提示")

rt = MondayRealtimeSystem()
h = rt.health()
scored = rt.score()

c1, c2 = st.columns(2)
c1.metric("数据源", h.get("active_source"))
c2.metric("行数", h.get("rows"))
st.metric("实时状态", "实时ON" if h.get("live_ready") else "备用模式")

if scored.empty:
    st.warning("暂无数据。")
else:
    buy = scored[scored["AI信号"].isin(["重点买入关注", "买入观察"])]
    risk = scored[scored["AI信号"] == "风险回避"]
    st.success(f"扫描 {len(scored)} 只；买入关注 {len(buy)}；风险回避 {len(risk)}。")

    st.subheader("AI重点")
    for _, r in scored.head(12).iterrows():
        text = f"{r.get('AI信号')}｜{r.get('code')} {r.get('name')}｜分数 {r.get('LJC实时分')}｜仓位 {r.get('建议仓位')}"
        if r.get("AI信号") in ["重点买入关注", "买入观察"]:
            st.success(text)
        elif r.get("AI信号") == "风险回避":
            st.error(text)
        else:
            st.info(text)
        st.caption(r.get("理由"))

with st.expander("健康检查"):
    st.json(h)
