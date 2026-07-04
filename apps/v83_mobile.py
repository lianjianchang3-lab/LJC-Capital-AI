import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.v83 import V83ProviderManager, AlphaValidationCenter, PortfolioAI, InstitutionCommittee

st.set_page_config(page_title="LJC V8.3 Mobile", page_icon="📱", layout="centered")

st.title("📱 LJC V8.3 Mobile")
st.caption("手机实战工作台｜信号｜仓位｜风险｜投委会")

data = V83ProviderManager().health()
alpha = AlphaValidationCenter().validate()
portfolio = PortfolioAI().propose()
committee = InstitutionCommittee().meeting()

st.subheader("今日状态")
c1, c2 = st.columns(2)
c1.metric("数据模式", data.get("mode"))
c2.metric("行情行数", data.get("quotes_rows"))

st.subheader("组合建议")
st.metric("现金比例", portfolio.get("cash_weight"))
st.metric("观察数量", portfolio.get("watch_count"))
st.json({"risk_budget": portfolio.get("risk_budget")})

st.subheader("投委会结论")
st.success(committee.get("final_summary"))
votes = committee.get("votes", [])
if votes:
    st.dataframe(pd.DataFrame(votes), use_container_width=True, hide_index=True)

st.subheader("Alpha Cards")
cards = alpha.get("cards", [])
if cards:
    for card in cards[:8]:
        with st.expander(f"{card.get('code')} {card.get('name')}｜{card.get('suggestion')}｜{card.get('confidence')}"):
            st.write(f"Score: {card.get('investment_score')}")
            st.write(f"LIA: {card.get('lia')}")
            st.write(f"Capital: {card.get('capital')}")
            st.write(f"Risk: {card.get('risk')}")
            st.write(f"Why: {card.get('why')}")
else:
    st.warning("暂无 Alpha Cards")
