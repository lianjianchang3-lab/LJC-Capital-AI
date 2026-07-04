import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd

from core.v83 import V83ProviderManager, AlphaValidationCenter, LearningEngine, PortfolioAI, InstitutionCommittee

st.set_page_config(page_title="LJC V8.3 Autonomous Engine", page_icon="🤖", layout="wide")

st.title("🤖 LJC Capital AI V8.3 Autonomous Investment Engine")
st.caption("M1 Data｜M2 Alpha Validation｜M3 Learning｜M4 Portfolio AI｜M5 Institution Committee")

tabs = st.tabs([
    "M1 Realtime Data Engine",
    "M2 Alpha Validation",
    "M3 Learning Engine",
    "M4 Portfolio AI",
    "M5 Institution Committee",
    "V8.3 Validation"
])

with tabs[0]:
    st.header("M1 Realtime Data Engine")
    st.json(V83ProviderManager().health())

with tabs[1]:
    st.header("M2 Alpha Validation Center")
    result = AlphaValidationCenter().validate()
    st.json({"status": result.get("status")})
    st.dataframe(pd.DataFrame(result.get("cards", [])), use_container_width=True, hide_index=True)

with tabs[2]:
    st.header("M3 AI Learning Engine")
    engine = LearningEngine()
    if st.button("Run Calibration"):
        st.json(engine.calibrate())
    st.subheader("Latest Model")
    st.json(engine.latest())

with tabs[3]:
    st.header("M4 Portfolio AI")
    capital = st.number_input("Capital", min_value=10000, value=1000000, step=10000)
    st.json(PortfolioAI(capital=capital).propose())

with tabs[4]:
    st.header("M5 Institution Committee")
    meeting = InstitutionCommittee().meeting()
    st.json({"final_summary": meeting.get("final_summary")})
    st.subheader("Votes")
    st.dataframe(pd.DataFrame(meeting.get("votes", [])), use_container_width=True, hide_index=True)
    st.subheader("Portfolio")
    st.json(meeting.get("portfolio"))

with tabs[5]:
    st.header("V8.3 Validation")
    st.success("V8.3 M1-M5 已加载")
    st.markdown("""
### 验收标准

- M1 Provider 健康状态可见
- M2 每只股票生成 Alpha Validation Card
- M3 可保存模型权重
- M4 可生成组合建议
- M5 可给出委员会投票
""")
