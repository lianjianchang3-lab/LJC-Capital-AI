import streamlit as st

from engine.dynamic_pool_engine import DynamicPoolEngine


def compact_style():
    st.markdown(
        """
        <style>
        .block-container {padding-top:.55rem; padding-bottom:.7rem; max-width:980px;}
        h1,h2,h3,h4 {margin-top:.15rem; margin-bottom:.15rem;}
        div[data-testid="stMetricValue"] {font-size:.95rem;}
        div[data-testid="stMetricLabel"] {font-size:.68rem;}
        .card {border:1px solid rgba(120,120,120,.25); border-radius:9px; padding:6px 8px; margin:3px 0; font-size:.84rem;}
        .line {display:flex; justify-content:space-between; gap:8px;}
        .muted {opacity:.72; font-size:.74rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_card(row):
    st.markdown(
        f"""
        <div class="card">
          <div class="line"><b>{row['code']} {row['name']}</b><span>{row['pool']}｜LCRI {row['lcri']}｜NAS {row['nas']}</span></div>
          <div class="line muted"><span>NPS {row['nps']}｜NDS {row['nds']}｜CCS {row['ccs']}</span><span>{row['action']}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home():
    st.set_page_config(page_title="LJC AI Pro Build008", page_icon="🚀", layout="wide")
    compact_style()

    engine = DynamicPoolEngine()
    data = engine.run()

    st.markdown("### 🚀 LJC AI Pro Build008")
    st.caption("Dynamic Pool Scoring｜NAS/NPS/NDS/CCS｜Compact Mobile")

    st.markdown("#### 🧠 Nova Commander")
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("买入", data["commander"]["buy"])
        c2.metric("做T", data["commander"]["t"])
        c3.metric("减仓", data["commander"]["reduce"])
        c4.metric("风险", data["commander"]["risk"])
        st.caption(data["commander"]["reason"])

    st.markdown("#### 💎 Diamond Core")
    for row in data["diamond_core"]:
        render_card(row)

    st.markdown("#### 🚀 Opportunity Pool")
    for row in data["opportunity_pool"]:
        render_card(row)

    st.markdown("#### 👀 Watch Pool")
    for row in data["watch_pool"]:
        render_card(row)

    st.markdown("#### 🔁 Upgrade / Demotion")
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("升级候选", len(data["upgrade_candidates"]))
        c2.metric("降级观察", len(data["demotion_candidates"]))
        c3.metric("核心池", len(data["diamond_core"]))
        c4.metric("机会池", len(data["opportunity_pool"]))
        st.caption(data["movement_summary"])

    st.markdown("#### ⚠ Risk Radar")
    with st.container(border=True):
        st.caption(data["risk_summary"])
