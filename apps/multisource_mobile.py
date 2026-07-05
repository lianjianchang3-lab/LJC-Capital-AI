import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import streamlit as st
from core.multisource import MultiSourceRealtimeHub

st.set_page_config(page_title="LJC 多源手机", page_icon="📱", layout="centered")
st.title("📱 LJC 多源实时")
hub = MultiSourceRealtimeHub()
h = hub.health()
s = hub.score()

c1,c2 = st.columns(2)
c1.metric("数据源", h["active_source"])
c2.metric("行数", h["rows"])

if s.empty:
    st.warning("暂无数据")
else:
    st.success(f"已扫描 {len(s)} 条，自动备用链路已启用。")
    for _, r in s.head(12).iterrows():
        txt = f"{r.get('AI信号')}｜{r.get('code')} {r.get('name')}｜{r.get('price')}｜{r.get('change_pct')}%｜分数{r.get('LJC实时分')}"
        if r.get("AI信号") in ["重点买入关注","买入观察"]:
            st.success(txt)
        elif r.get("AI信号") == "风险回避":
            st.error(txt)
        else:
            st.info(txt)

with st.expander("健康检查"):
    st.json(h)
