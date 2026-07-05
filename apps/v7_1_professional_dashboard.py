import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st
from core.enterprise import EnterpriseCommander

st.set_page_config(
    page_title="LJC V7.1 Pro Dashboard",
    page_icon="🧠",
    layout="wide",
)

st.markdown(
    """
<style>
.block-container {padding-top: 1.5rem; max-width: 1280px;}
.ljc-card {
    padding: 18px 20px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(34,45,65,0.08), rgba(34,45,65,0.02));
    border: 1px solid rgba(120,120,120,0.16);
    margin-bottom: 12px;
}
.ljc-title {font-size: 34px; font-weight: 800; margin-bottom: 0px;}
.ljc-subtitle {font-size: 14px; opacity: 0.65; margin-bottom: 18px;}
.good {color: #17803d; font-weight: 700;}
.warn {color: #b57900; font-weight: 700;}
.bad {color: #b00020; font-weight: 700;}
.small {font-size: 13px; opacity: 0.70;}
</style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data(ttl=8)
def load_snapshot():
    return EnterpriseCommander().snapshot()

snap = load_snapshot()
market = snap.get("market", {}) or {}
health = snap.get("radar_health", {}) or {}

st.markdown('<div class="ljc-title">🧠 LJC Capital AI Pro V7.1</div>', unsafe_allow_html=True)
st.markdown('<div class="ljc-subtitle">Professional Dashboard｜Enterprise Commander｜Market Radar｜DecisionHub</div>', unsafe_allow_html=True)

auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N", 5, 50, 20)
st.sidebar.markdown("---")
st.sidebar.write("已挂载服务：")
st.sidebar.code(", ".join(snap.get("services", [])) or "-")

c1, c2, c3, c4 = st.columns(4)
c1.metric("市场状态", market.get("state", "-"))
c2.metric("建议仓位", market.get("position", "-"))
c3.metric("LCRI均分", market.get("lcri_avg", "-"))
c4.metric("扫描数量", health.get("lcri_count", 0))

st.markdown(
    f"""
<div class="ljc-card">
<span class="good">今日总控：</span>
{snap.get("summary", "-")}
</div>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs(["总控", "LCRI榜", "AI交易榜", "机构共振", "风险雷达", "执行计划", "系统状态"])

def df_from(key):
    return pd.DataFrame(snap.get(key, []) or [])

def show_table(df, cols=None):
    if df.empty:
        st.warning("暂无数据")
        return
    if cols:
        use = [c for c in cols if c in df.columns]
        if use:
            df = df[use]
    st.dataframe(df.head(top), use_container_width=True, hide_index=True)

with tabs[0]:
    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("📌 今日重点")
        lcri = df_from("lcri_top")
        if not lcri.empty:
            for _, r in lcri.head(8).iterrows():
                action = r.get("Action", r.get("执行建议", "观察"))
                code = r.get("code", "")
                name = r.get("name", "")
                score = r.get("LCRI Score", "")
                pos = r.get("Position", r.get("建议仓位V5", ""))
                st.info(f"{action}｜{code} {name}｜LCRI {score}｜仓位 {pos}")
        else:
            st.warning("暂无 LCRI 数据")
    with right:
        st.subheader("⚠️ 风险摘要")
        risk = df_from("risk_top")
        if not risk.empty:
            show_table(risk, ["code", "name", "风险热度", "risk_score", "LCRI Score", "Action"])
        else:
            st.success("暂无明显风险")

with tabs[1]:
    st.subheader("📈 LCRI Top")
    show_table(df_from("lcri_top"))

with tabs[2]:
    st.subheader("🤖 AI Trader Top")
    show_table(df_from("trader_top"))

with tabs[3]:
    st.subheader("🏛️ 机构共振 Top")
    show_table(df_from("institution_top"))

with tabs[4]:
    st.subheader("⚠️ 风险雷达")
    show_table(df_from("risk_top"))

with tabs[5]:
    st.subheader("🧾 今日执行计划")
    trader = df_from("trader_top")
    if trader.empty:
        lcri = df_from("lcri_top")
        if lcri.empty:
            st.warning("暂无执行计划")
        else:
            for i, (_, r) in enumerate(lcri.head(10).iterrows(), 1):
                st.write(f"{i}. {r.get('code')} {r.get('name')}｜{r.get('Action','观察')}｜LCRI {r.get('LCRI Score')}｜仓位 {r.get('Position','-')}")
                st.caption(r.get("Reason") or r.get("LCRI Evidence") or "")
    else:
        for i, (_, r) in enumerate(trader.head(10).iterrows(), 1):
            st.write(f"{i}. {r.get('code')} {r.get('name')}｜{r.get('执行建议','观察')}｜强度 {r.get('AI交易强度','-')}｜仓位 {r.get('建议仓位V5','-')}")
            st.caption(f"买点 {r.get('第一买点','-')}/{r.get('第二买点','-')}｜止损 {r.get('止损价','-')}｜目标 {r.get('第一止盈','-')}/{r.get('第二止盈','-')}")

with tabs[6]:
    st.subheader("🛠 系统状态")
    st.json({
        "market": market,
        "health": health,
        "services": snap.get("services", []),
        "configs": snap.get("configs", {}),
    })

if auto:
    time.sleep(sec)
    st.rerun()
