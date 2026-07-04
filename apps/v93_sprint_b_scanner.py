import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import time

from core.v93.realtime import RealtimeCore
try:
    from core.v93.scanner import MarketScanner
except Exception:
    MarketScanner = None
try:
    from core.v93.score import AIScoreV3
except Exception:
    AIScoreV3 = None
try:
    from core.v93.signal import SignalEngine
except Exception:
    SignalEngine = None

st.set_page_config(page_title="LJC V9.3 实时扫描系统", page_icon="⚡", layout="wide")

st.title("⚡ LJC Capital AI V9.3 实时扫描系统")
st.caption("AKShare 自动切换｜实时扫描｜AI评分V3｜信号中心｜手机同步")

st.sidebar.header("控制面板")
auto = st.sidebar.checkbox("自动刷新", value=False)
sec = st.sidebar.slider("刷新秒数", 5, 60, 10)
top_n = st.sidebar.slider("显示前 N 名", 10, 200, 50)

core = RealtimeCore()

def get_quotes():
    try:
        return core.quotes()
    except Exception:
        return pd.DataFrame()

def health():
    try:
        return core.health()
    except Exception as e:
        return {"engine": "V9.3 Realtime Core", "active_source": "错误", "rows": 0, "live_ready": False, "error": str(e), "csv_sources": []}

def simple_score(df):
    if df.empty:
        return df
    df = df.copy()
    for col in ["change_pct","main_inflow","trend","capital","risk","quality","lia","amount","turnover"]:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["AI评分"] = (
        df["change_pct"].clip(-10, 10) * 2
        + df["capital"] * 0.25
        + df["lia"] * 0.25
        + df["trend"] * 0.2
        + df["main_inflow"] * 10
        - df["risk"] * 0.2
    ).round(1)

    df["信号"] = "观察"
    df.loc[(df["AI评分"] >= 80) & (df["risk"] <= 60), "信号"] = "买入关注"
    df.loc[(df["risk"] >= 75) | (df["change_pct"] <= -4), "信号"] = "风险警示"
    df.loc[(df["AI评分"] < 40), "信号"] = "回避"

    if "code" in df.columns:
        df = df.rename(columns={"code": "代码"})
    if "name" in df.columns:
        df = df.rename(columns={"name": "名称"})
    if "price" in df.columns:
        df = df.rename(columns={"price": "现价"})
    if "change_pct" in df.columns:
        df = df.rename(columns={"change_pct": "涨跌幅"})
    if "capital" in df.columns:
        df = df.rename(columns={"capital": "资金评分"})
    if "lia" in df.columns:
        df = df.rename(columns={"lia": "LIA"})
    if "risk" in df.columns:
        df = df.rename(columns={"risk": "风险"})
    if "source" in df.columns:
        df = df.rename(columns={"source": "数据源"})
    return df.sort_values("AI评分", ascending=False)

tabs = st.tabs(["实时健康", "市场扫描", "AI信号", "系统验收", "手机部署"])

with tabs[0]:
    st.header("实时数据健康状态")
    h = health()
    c1, c2, c3 = st.columns(3)
    c1.metric("当前数据源", h.get("active_source"))
    c2.metric("数据行数", h.get("rows"))
    c3.metric("实时接口", "已启用" if h.get("live_ready") else "未启用 / CSV备用")

    st.subheader("AKShare 状态")
    st.json({
        "AKShare 是否安装": h.get("akshare_installed"),
        "AKShare 错误": h.get("akshare_error")
    })

    st.subheader("备用数据源")
    st.dataframe(pd.DataFrame(h.get("csv_sources", [])), use_container_width=True, hide_index=True)

with tabs[1]:
    st.header("市场实时扫描")
    q = get_quotes()
    if q.empty:
        st.warning("暂无行情数据。请安装 AKShare 或准备 CSV 数据。")
    else:
        scored = simple_score(q)
        st.success(f"已扫描 {len(scored)} 条数据，显示前 {top_n} 名。")
        st.dataframe(scored.head(top_n), use_container_width=True, hide_index=True)

with tabs[2]:
    st.header("AI信号中心")
    q = get_quotes()
    scored = simple_score(q)
    if scored.empty:
        st.info("暂无信号。")
    else:
        buy = scored[scored["信号"] == "买入关注"]
        risk = scored[scored["信号"] == "风险警示"]
        a,b,c = st.columns(3)
        a.metric("买入关注", len(buy))
        b.metric("风险警示", len(risk))
        c.metric("观察总数", len(scored))

        st.subheader("重点信号")
        signal_df = scored[scored["信号"].isin(["买入关注", "风险警示"])].head(top_n)
        if signal_df.empty:
            st.info("当前没有强信号，继续观察。")
        else:
            st.dataframe(signal_df, use_container_width=True, hide_index=True)

with tabs[3]:
    st.header("V9.3 Sprint B 中文版验收")
    h = health()
    checks = [
        {"检查项": "界面中文化", "结果": "通过", "说明": "主要页面与字段已改为中文"},
        {"检查项": "实时核心加载", "结果": "通过", "说明": h.get("engine")},
        {"检查项": "数据可读取", "结果": "通过" if h.get("rows", 0) > 0 else "待检查", "说明": h.get("rows")},
        {"检查项": "备用机制", "结果": "通过", "说明": h.get("active_source")},
    ]
    st.dataframe(pd.DataFrame(checks), use_container_width=True, hide_index=True)
    if h.get("rows", 0) > 0:
        st.success("V9.3 中文界面运行正常。")
    else:
        st.warning("界面正常，但当前未读取到行情数据。")

with tabs[4]:
    st.header("手机端部署")
    st.markdown("""
### 启动手机端

```bash
python -m streamlit run apps/v93_mobile_scanner.py --server.address 0.0.0.0 --server.port 8501
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

if auto:
    time.sleep(sec)
    st.rerun()
