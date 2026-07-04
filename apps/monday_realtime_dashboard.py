import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.monday_realtime import MondayRealtimeSystem

st.set_page_config(page_title="LJC 周一实时系统", page_icon="🟢", layout="wide")
st.title("🟢 LJC Capital AI 周一实时数据系统")
st.caption("目标：明天完成部署，周一可用｜AKShare实时行情｜自动缓存｜CSV备用｜手机端")

sys_rt = MondayRealtimeSystem()

st.sidebar.header("控制面板")
auto = st.sidebar.checkbox("自动刷新", value=True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N名", 10, 300, 80)

tabs = st.tabs(["总控台", "实时行情", "AI实时评分", "健康检查", "手机部署", "周一使用流程"])

with tabs[0]:
    h = sys_rt.health()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("当前数据源", h.get("active_source"))
    c2.metric("数据行数", h.get("rows"))
    c3.metric("实时状态", "实时ON" if h.get("live_ready") else "备用模式")
    c4.metric("更新时间", h.get("updated_at"))
    if h.get("rows", 0) > 0:
        st.success("系统已可用。周一若AKShare正常，将自动使用实时行情；若网络异常，将自动使用缓存/CSV备用。")
    else:
        st.error("未读取到行情数据。需要检查网络、AKShare或CSV备用文件。")

with tabs[1]:
    q = sys_rt.quotes(prefer_live=True)
    if q.empty:
        st.warning("暂无行情数据。")
    else:
        st.dataframe(q.head(top), use_container_width=True, hide_index=True)

with tabs[2]:
    scored = sys_rt.score()
    if scored.empty:
        st.warning("暂无评分数据。")
    else:
        buy = scored[scored["AI信号"].isin(["重点买入关注", "买入观察"])]
        risk = scored[scored["AI信号"] == "风险回避"]
        a,b,c = st.columns(3)
        a.metric("买入关注", len(buy))
        b.metric("风险回避", len(risk))
        c.metric("样本", len(scored))
        st.dataframe(scored.head(top), use_container_width=True, hide_index=True)

with tabs[3]:
    result = sys_rt.smoke_test()
    st.json(result.get("health"))
    st.dataframe(pd.DataFrame(result.get("checks")), use_container_width=True, hide_index=True)

with tabs[4]:
    st.markdown("""
### 手机端启动命令

```bash
cd ~/LJC-Capital-AI
source .venv/bin/activate
export PYTHONPATH=$PWD
python -m streamlit run apps/monday_realtime_mobile.py --server.address 0.0.0.0 --server.port 8501
```

### 查看 Mac IP

```bash
ipconfig getifaddr en0
```

### 手机 Safari 打开

```text
http://你的Mac_IP:8501
```
""")

with tabs[5]:
    st.markdown("""
## 周一使用流程

### 09:00 前
1. 打开电脑端 `monday_realtime_dashboard.py`
2. 看“健康检查”是否通过
3. 确认“当前数据源”是否为 `AKShare东方财富实时`

### 09:25
1. 打开手机端
2. 确认数据行数大于 0
3. 看 AI 实时评分 Top 列表

### 09:30-11:30 / 13:00-15:00
1. 保持电脑端或手机端运行
2. 自动刷新 30 秒一次
3. 强信号只作为研究辅助，实盘前人工确认

### 如果实时源失败
系统会自动降级到：
- Monday实时缓存
- V10.5缓存
- V101缓存
- quotes_realtime.csv
- data/quotes.csv
""")

if auto:
    time.sleep(sec)
    st.rerun()
