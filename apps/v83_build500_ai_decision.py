import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd

from core.v83.score_v4 import AIScoreV4
from core.v83.portfolio_pro import PortfolioManagerPro
from core.v83.committee_v2 import InstitutionCommitteeV2
from core.v83.decision import AutonomousCommander
from core.v83.mobile import MobileConfig

st.set_page_config(page_title="LJC V8.3 Build500", page_icon="🧠", layout="wide")

st.title("🧠 LJC Capital AI V8.3 Build301-500")
st.caption("AI Score V4｜Portfolio Manager Pro｜Institution Committee V2｜Autonomous Commander｜Test & Mobile Deploy")

tabs = st.tabs([
    "301-340 AI Score V4",
    "341-380 Portfolio Pro",
    "381-420 Committee V2",
    "421-500 Commander",
    "Test Center",
    "Mobile Deploy"
])

with tabs[0]:
    st.header("AI Score V4")
    df = AIScoreV4().table()
    st.dataframe(df, use_container_width=True, hide_index=True)

with tabs[1]:
    st.header("Portfolio Manager Pro")
    capital = st.number_input("Capital", min_value=10000, value=1000000, step=10000)
    plan = PortfolioManagerPro(capital).plan()
    a,b,c = st.columns(3)
    a.metric("Total Position", plan.get("total_position_weight"))
    b.metric("Cash Weight", plan.get("cash_weight"))
    c.metric("Cash Amount", plan.get("cash_amount"))
    st.warning(plan.get("risk_budget"))
    st.dataframe(pd.DataFrame(plan.get("positions", [])), use_container_width=True, hide_index=True)

with tabs[2]:
    st.header("Institution Committee V2")
    vote = InstitutionCommitteeV2().vote()
    st.dataframe(pd.DataFrame(vote.get("votes", [])), use_container_width=True, hide_index=True)

with tabs[3]:
    st.header("Autonomous Commander")
    plan = AutonomousCommander().daily_plan()
    st.success(plan.get("final_instruction"))
    st.warning(plan.get("risk_warning"))
    st.json({"time": plan.get("time"), "version": plan.get("version"), "data_health": plan.get("data_health")})
    st.subheader("Portfolio Plan")
    st.json(plan.get("portfolio_plan"))

with tabs[4]:
    st.header("Test Center")
    checks = []
    try:
        df = AIScoreV4().table()
        checks.append({"check": "AI Score V4", "pass": not df.empty, "detail": f"rows={len(df)}"})
    except Exception as e:
        checks.append({"check": "AI Score V4", "pass": False, "detail": str(e)})
    try:
        p = PortfolioManagerPro().plan()
        checks.append({"check": "Portfolio Pro", "pass": p.get("status") == "OK", "detail": p.get("risk_budget")})
    except Exception as e:
        checks.append({"check": "Portfolio Pro", "pass": False, "detail": str(e)})
    try:
        v = InstitutionCommitteeV2().vote()
        checks.append({"check": "Committee V2", "pass": v.get("status") == "OK", "detail": f"votes={len(v.get('votes', []))}"})
    except Exception as e:
        checks.append({"check": "Committee V2", "pass": False, "detail": str(e)})
    try:
        c = AutonomousCommander().daily_plan()
        checks.append({"check": "Commander", "pass": "final_instruction" in c, "detail": c.get("final_instruction")})
    except Exception as e:
        checks.append({"check": "Commander", "pass": False, "detail": str(e)})

    st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)
    if all(x["pass"] for x in checks):
        st.success("Build301-500 测试通过，可以进入手机部署。")
    else:
        st.error("仍有检查未通过。")

with tabs[5]:
    st.header("Mobile Deploy")
    st.json(MobileConfig().guide())
    st.markdown("""
### 本地手机访问

```bash
cd ~/LJC-Capital-AI
export PYTHONPATH=$PWD
python -m streamlit run apps/v83_build500_ai_decision.py --server.address 0.0.0.0
```

然后手机与电脑连接同一 Wi-Fi，打开终端里的 Network URL。

### 云端部署

GitHub 推送成功后，Streamlit Cloud 入口文件选择：

```text
apps/v83_build500_ai_decision.py
```
""")
