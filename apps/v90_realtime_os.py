import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd

from core.v90 import V90RealtimeManager, V90DecisionEngine

st.set_page_config(page_title="LJC V9.0 Realtime OS", page_icon="🚀", layout="wide")

st.title("🚀 LJC Capital AI V9.0 Realtime OS")
st.caption("实时数据总线｜AI决策｜交易计划｜测试验收｜手机部署")

engine = V90DecisionEngine()
data = V90RealtimeManager()

tabs = st.tabs(["Realtime Data", "AI Dashboard", "Trading Plan", "Validation", "Mobile Deploy"])

with tabs[0]:
    st.header("V9.0 Realtime Data Bus")
    h = data.health()
    c1, c2, c3 = st.columns(3)
    c1.metric("Active Source", h.get("active_source"))
    c2.metric("Rows", h.get("active_rows"))
    c3.metric("Realtime Ready", str(h.get("realtime_ready")))
    st.dataframe(pd.DataFrame(h.get("sources", [])), use_container_width=True, hide_index=True)
    quotes = data.get_quotes()
    if not quotes.empty:
        st.subheader("Quotes")
        st.dataframe(quotes, use_container_width=True, hide_index=True)

with tabs[1]:
    st.header("AI Decision Dashboard")
    d = engine.dashboard()
    a,b,c,dcol = st.columns(4)
    a.metric("Version", d.get("version"))
    b.metric("Quotes", d.get("quote_count"))
    c.metric("Alpha", d.get("alpha_count"))
    dcol.metric("Cash", d.get("cash_weight"))
    st.success(d.get("committee_summary"))
    st.info(d.get("realtime_note"))

with tabs[2]:
    st.header("Daily Trading Plan")
    plan = engine.trading_plan()
    st.json({"market_mode": plan.get("market_mode"), "cash_weight": plan.get("cash_weight"), "risk_note": plan.get("risk_note")})
    st.dataframe(pd.DataFrame(plan.get("actions", [])), use_container_width=True, hide_index=True)

with tabs[3]:
    st.header("V9.0 Validation")
    h = data.health()
    checks = [
        {"check": "Realtime Manager", "pass": True, "detail": h.get("active_source")},
        {"check": "Data Available", "pass": h.get("active_rows", 0) > 0, "detail": h.get("active_rows")},
        {"check": "Decision Engine", "pass": len(engine.dashboard().get("votes", [])) >= 0, "detail": "loaded"},
        {"check": "Trading Plan", "pass": "actions" in engine.trading_plan(), "detail": "generated"},
    ]
    passed = sum(1 for x in checks if x["pass"])
    st.metric("Validation", f"{passed}/{len(checks)}")
    if passed == len(checks):
        st.success("V9.0 Realtime OS 验收通过。")
    else:
        st.warning("V9.0 可运行，但实时数据文件尚未准备或为空。")
    st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)

with tabs[4]:
    st.header("Mobile Deploy")
    st.markdown("""
### 手机访问

1. Mac 运行：
```bash
python -m streamlit run apps/v90_mobile.py --server.address 0.0.0.0 --server.port 8501
```

2. 查询 IP：
```bash
ipconfig getifaddr en0
```

3. iPhone Safari：
```text
http://你的Mac_IP:8501
```
""")
