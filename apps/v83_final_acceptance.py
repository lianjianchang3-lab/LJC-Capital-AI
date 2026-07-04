import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from datetime import datetime

from core.v83 import V83ProviderManager, AlphaValidationCenter, LearningEngine, PortfolioAI, InstitutionCommittee

st.set_page_config(page_title="LJC V8.3 Final Acceptance", page_icon="✅", layout="wide")

st.title("✅ LJC Capital AI V8.3 Final Acceptance")
st.caption("V8.3 完成验收｜M1-M5｜测试｜手机部署｜Final Candidate")

tabs = st.tabs([
    "Final Dashboard",
    "M1 Data Test",
    "M2 Alpha Test",
    "M3 Learning Test",
    "M4 Portfolio Test",
    "M5 Committee Test",
    "Mobile Deploy",
    "Final Report"
])

def safe_call(fn):
    try:
        return True, fn()
    except Exception as e:
        return False, {"error": str(e)}

tests = []
ok, data = safe_call(lambda: V83ProviderManager().health())
tests.append({"module": "M1 Data Engine", "pass": ok, "detail": data})

ok, alpha = safe_call(lambda: AlphaValidationCenter().validate())
tests.append({"module": "M2 Alpha Validation", "pass": ok and "cards" in alpha, "detail": {"status": alpha.get("status"), "cards": len(alpha.get("cards", [])) if isinstance(alpha, dict) else 0}})

ok, model = safe_call(lambda: LearningEngine().calibrate())
tests.append({"module": "M3 Learning Engine", "pass": ok and "weights" in model, "detail": model})

ok, portfolio = safe_call(lambda: PortfolioAI().propose())
tests.append({"module": "M4 Portfolio AI", "pass": ok and "allocations" in portfolio, "detail": {"allocations": len(portfolio.get("allocations", [])) if isinstance(portfolio, dict) else 0, "cash_weight": portfolio.get("cash_weight") if isinstance(portfolio, dict) else None}})

ok, committee = safe_call(lambda: InstitutionCommittee().meeting())
tests.append({"module": "M5 Institution Committee", "pass": ok and "votes" in committee, "detail": {"votes": len(committee.get("votes", [])) if isinstance(committee, dict) else 0, "summary": committee.get("final_summary") if isinstance(committee, dict) else None}})

all_pass = all(t["pass"] for t in tests)

with tabs[0]:
    st.header("V8.3 Final Dashboard")
    a,b,c,d = st.columns(4)
    a.metric("Version", "V8.3 Final Candidate")
    b.metric("Tests", f"{sum(t['pass'] for t in tests)}/{len(tests)}")
    c.metric("Status", "PASS" if all_pass else "CHECK")
    d.metric("Time", datetime.now().strftime("%H:%M"))
    if all_pass:
        st.success("V8.3 M1-M5 已通过最终验收，可以进入手机部署。")
    else:
        st.warning("部分测试未完全通过，请查看各模块详情。")
    st.dataframe(pd.DataFrame([{"module":t["module"], "pass":t["pass"], "detail":str(t["detail"])[:120]} for t in tests]), use_container_width=True, hide_index=True)

with tabs[1]:
    st.header("M1 Data Engine Test")
    st.json(tests[0]["detail"])

with tabs[2]:
    st.header("M2 Alpha Validation Test")
    st.json(alpha if isinstance(alpha, dict) else {})

with tabs[3]:
    st.header("M3 Learning Engine Test")
    st.json(model if isinstance(model, dict) else {})

with tabs[4]:
    st.header("M4 Portfolio AI Test")
    st.json(portfolio if isinstance(portfolio, dict) else {})

with tabs[5]:
    st.header("M5 Institution Committee Test")
    if isinstance(committee, dict):
        st.json({"final_summary": committee.get("final_summary")})
        st.dataframe(pd.DataFrame(committee.get("votes", [])), use_container_width=True, hide_index=True)
        st.subheader("Portfolio")
        st.json(committee.get("portfolio"))

with tabs[6]:
    st.header("手机部署 Mobile Deploy")
    st.markdown("""
### 手机访问方式

电脑和手机必须连接同一个 Wi-Fi / 热点。

1. 在 Mac 终端运行：

```bash
cd ~/LJC-Capital-AI
source .venv/bin/activate
export PYTHONPATH=$PWD
python -m streamlit run apps/v83_mobile.py --server.address 0.0.0.0 --server.port 8501
```

2. 查询 Mac 局域网 IP：

```bash
ipconfig getifaddr en0
```

如果你用手机热点，可能是：

```bash
ipconfig getifaddr en1
```

3. iPhone Safari 输入：

```text
http://你的Mac_IP:8501
```

例如：

```text
http://192.168.1.8:8501
```
""")
    st.info("手机页面已生成：apps/v83_mobile.py")

with tabs[7]:
    st.header("Final Report")
    report = f"""
# LJC Capital AI V8.3 Final Acceptance Report

- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Version: V8.3 Final Candidate
- Tests Passed: {sum(t['pass'] for t in tests)}/{len(tests)}
- Overall: {'PASS' if all_pass else 'CHECK'}

## Modules
""" + "\n".join([f"- {t['module']}: {'PASS' if t['pass'] else 'CHECK'}" for t in tests]) + """

## Mobile Deploy
Use `scripts/start_v83_mobile.command` and open `http://Mac_IP:8501` on iPhone.

## Risk Note
Current system is research/decision support. CSV or adapter data must be checked before live trading.
"""
    st.code(report, language="markdown")
