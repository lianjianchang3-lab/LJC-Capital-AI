import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

import streamlit as st
import pandas as pd
from core.v11 import DataCenterV11,AICenterV11,PortfolioCenterV11,MarketCenterV11,RiskCenterV11

st.set_page_config(page_title="LJC V11 手机端", page_icon="📱", layout="centered")
st.title("📱 LJC V11 机构终端")
st.caption("一屏看数据｜AI｜组合｜风险｜热点")

h=DataCenterV11().health(); p=PortfolioCenterV11().plan(); r=RiskCenterV11().assess()
c1,c2=st.columns(2)
c1.metric("数据源",h["active_source"]); c2.metric("行数",h["rows"])
st.metric("建议现金",f"{p['cash_weight']:.0%}")
st.warning(r.get("summary")); st.success(p.get("summary"))

ai=AICenterV11().decisions()
st.subheader("AI重点")
for x in ai.get("items",[])[:10]:
    text=f"{x.get('AI决策')}｜{x.get('code')} {x.get('name')}｜仓位 {x.get('建议仓位')}｜分数 {x.get('AI综合分')}"
    if x.get("AI决策") in ["重点买入关注","买入观察"]:
        st.success(text)
    elif x.get("AI决策")=="风险回避":
        st.error(text)
    else:
        st.info(text)
    st.caption(x.get("理由"))

with st.expander("热点行业"):
    st.dataframe(pd.DataFrame(MarketCenterV11().snapshot().get("hot_sectors",[])).head(10), use_container_width=True, hide_index=True)
