import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.v93.realtime import RealtimeCore

st.set_page_config(page_title="LJC V9.3 手机端", page_icon="📱", layout="centered")

st.title("📱 LJC V9.3 手机实时扫描")
st.caption("实时数据｜AI评分｜买入关注｜风险提示")

core = RealtimeCore()

def get_health():
    try:
        return core.health()
    except Exception as e:
        return {"active_source": "错误", "rows": 0, "live_ready": False, "error": str(e)}

def get_quotes():
    try:
        return core.quotes()
    except Exception:
        return pd.DataFrame()

def score(df):
    if df.empty:
        return df
    df = df.copy()
    for col in ["change_pct","main_inflow","trend","capital","risk","quality","lia"]:
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
    df = df.sort_values("AI评分", ascending=False)
    return df

h = get_health()
q = get_quotes()
df = score(q)

st.subheader("今日状态")
c1, c2 = st.columns(2)
c1.metric("数据源", h.get("active_source"))
c2.metric("行数", h.get("rows"))
st.metric("实时接口", "已启用" if h.get("live_ready") else "CSV备用")

st.subheader("AI结论")
if df.empty:
    st.warning("暂无数据。")
else:
    buy = df[df["信号"] == "买入关注"]
    risk = df[df["信号"] == "风险警示"]
    st.success(f"已扫描 {len(df)} 只；买入关注 {len(buy)}；风险警示 {len(risk)}。")

    st.subheader("重点机会")
    top = df.head(10)
    for _, r in top.iterrows():
        code = r.get("code", "")
        name = r.get("name", "")
        price = r.get("price", "")
        sig = r.get("信号", "")
        ai = r.get("AI评分", "")
        text = f"{sig}｜{code} {name}｜评分 {ai}｜现价 {price}"
        if sig == "买入关注":
            st.success(text)
        elif sig == "风险警示":
            st.error(text)
        else:
            st.info(text)

with st.expander("全部数据"):
    if not df.empty:
        show = df.copy()
        show = show.rename(columns={
            "code": "代码",
            "name": "名称",
            "price": "现价",
            "change_pct": "涨跌幅",
            "capital": "资金评分",
            "risk": "风险",
            "lia": "LIA",
            "source": "数据源",
        })
        st.dataframe(show.head(50), use_container_width=True, hide_index=True)
