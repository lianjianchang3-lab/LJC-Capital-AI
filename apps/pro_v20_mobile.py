import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.pro_v20 import ProDecisionCenter, ProWatchlistCenter, ProPortfolioCenter

st.set_page_config(page_title="LJC Pro V2 手机", page_icon="📱", layout="centered")
st.title("📱 LJC Pro V2.0")
st.caption("今日策略｜自选股｜我的持仓")

brief = ProDecisionCenter().morning_brief()
c1,c2 = st.columns(2)
c1.metric("AI均分", brief.get("market_score"))
c2.metric("仓位", brief.get("position"))
st.success(brief.get("summary"))

st.subheader("自选股作战")
watch = ProWatchlistCenter().analyze()
if watch.empty:
    st.warning("暂无自选股数据")
else:
    for _, x in watch.head(8).iterrows():
        text = f"{x.get('正式建议','观察')}｜{x.get('code')} {x.get('name')}｜Alpha {x.get('LJC Alpha Score')}｜仓位 {x.get('正式仓位','')}"
        if x.get("正式建议") == "买入关注":
            st.success(text)
        elif x.get("正式建议") == "减仓/回避":
            st.error(text)
        else:
            st.info(text)
        st.caption(x.get("证据",""))

with st.expander("我的持仓"):
    p = ProPortfolioCenter().analyze()
    st.write(p.get("summary"))
    st.dataframe(pd.DataFrame(p.get("holdings",[])), use_container_width=True, hide_index=True)
