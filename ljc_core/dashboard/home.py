import streamlit as st
from ljc_core.engine.decision_engine import DecisionEngine


def _style():
    st.markdown('''
    <style>
    .block-container {padding-top:.55rem; padding-bottom:.7rem; max-width:980px;}
    h1,h2,h3 {margin-top:.12rem; margin-bottom:.12rem;}
    div[data-testid="stMetricValue"] {font-size:1rem;}
    div[data-testid="stMetricLabel"] {font-size:.68rem;}
    .card {border:1px solid rgba(120,120,120,.25); border-radius:9px; padding:7px 9px; margin:4px 0; font-size:.85rem;}
    .muted {opacity:.72; font-size:.74rem;}
    </style>
    ''', unsafe_allow_html=True)


def _card(row):
    st.markdown(
        f'''<div class="card"><b>{row["code"]} {row["name"]}</b>｜{row["pool"]}｜LIA {row["lia"]}｜资金健康 {row["capital_health"]}<br>
        <span class="muted">现价：{row["close"]}｜涨跌：{row["change_pct"]}%｜动作：{row["action"]}</span><br>
        <span class="muted">1日 {row["mf_1d"]}亿｜3日 {row["mf_3d"]}亿｜5日 {row["mf_5d"]}亿｜{row["capital_state"]}</span><br>
        <span class="muted">证据：{row["evidence"]}</span></div>''',
        unsafe_allow_html=True,
    )


def render_home():
    st.set_page_config(page_title="LJC Capital AI Pro V4.0", page_icon="🚀", layout="wide")
    _style()
    data = DecisionEngine().run()
    wr = data["war_room"]

    st.markdown("### 🚀 LJC Capital AI Pro V4.0")
    st.caption("Core Clean Edition｜统一 ljc_core｜CSV数据驱动")

    st.markdown("#### 🧠 War Room")
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("市场", wr["market"])
        c2.metric("仓位", wr["position"])
        c3.metric("主线", wr["theme"])
        c4.metric("Confidence", wr["confidence"])
        st.caption(wr["mission"])

    st.markdown("#### 🚨 Alert Center")
    with st.container(border=True):
        for a in data["alerts"]:
            st.write(a)

    st.markdown("#### 💎 Diamond Core")
    for r in data["diamond"]:
        _card(r)

    st.markdown("#### 🚀 Opportunity Pool")
    for r in data["opportunity"]:
        _card(r)

    st.markdown("#### 👀 Watch")
    for r in data["watch"]:
        _card(r)

    st.markdown("#### 📊 数据说明")
    with st.container(border=True):
        st.caption("V4.0 已统一入口：ljc_core。数据优先读取项目 data/，没有则读取 ljc_core/data/。")
