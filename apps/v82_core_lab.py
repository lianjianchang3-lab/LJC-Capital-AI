import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd

from core.realtime import RealtimeProviderManager
from core.calibration import ModelCalibrator
from core.backtest_v2 import SignalBacktester

st.set_page_config(page_title="LJC V8.2 Core Lab", page_icon="🧪", layout="wide")

st.title("🧪 LJC Capital AI V8.2 Core Lab")
st.caption("三项核心能力：实时数据源｜评分模型校准｜信号回测验证")

tabs = st.tabs(["1 Realtime Provider", "2 Model Calibration", "3 Signal Backtest", "Core Validation"])

with tabs[0]:
    st.header("实时行情数据源 Adapter")
    rt = RealtimeProviderManager().snapshot()
    st.json(rt)
    st.info("当前先使用 data/realtime/quotes_realtime.csv 作为实时数据适配层。以后可以替换为真实API。")

with tabs[1]:
    st.header("评分模型校准")
    result = ModelCalibrator().run()
    st.json({"status": result.get("status"), "metrics": result.get("metrics"), "instruction": result.get("instruction")})
    if result.get("bucket_summary"):
        st.dataframe(pd.DataFrame(result.get("bucket_summary")), use_container_width=True, hide_index=True)
    if result.get("table"):
        st.dataframe(pd.DataFrame(result.get("table")), use_container_width=True, hide_index=True)

with tabs[2]:
    st.header("信号回测系统")
    result = SignalBacktester().run()
    st.json({"status": result.get("status"), "summary": result.get("summary"), "instruction": result.get("instruction"), "missing": result.get("missing")})
    if result.get("trades"):
        st.dataframe(pd.DataFrame(result.get("trades")), use_container_width=True, hide_index=True)

with tabs[3]:
    st.header("Core Validation")
    st.success("V8.2 Core Lab 已加载")
    st.markdown("""
### 当前优先级

1. 接入实时行情 Provider：先统一接口，再替换数据源。
2. 校准评分模型：验证 investment_score / LIA 是否能解释未来收益。
3. 建立回测系统：验证 WATCH_BUY / BUY / REDUCE 信号的胜率、收益、最大亏损。

### 启动方式

```bash
cd ~/LJC-Capital-AI
python -m streamlit run apps/v82_core_lab.py
```
""")
