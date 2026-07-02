import streamlit as st

from engine.v31_decision_os import V31DecisionOS


def compact_style():
    st.markdown(
        """
        <style>
        .block-container {padding-top:.55rem; padding-bottom:.75rem; max-width:980px;}
        h1,h2,h3,h4 {margin-top:.15rem; margin-bottom:.15rem;}
        div[data-testid="stMetricValue"] {font-size:.96rem;}
        div[data-testid="stMetricLabel"] {font-size:.68rem;}
        .card {border:1px solid rgba(120,120,120,.24); border-radius:9px; padding:6px 8px; margin:4px 0; font-size:.84rem;}
        .line {display:flex; justify-content:space-between; gap:8px;}
        .muted {opacity:.72; font-size:.74rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_stock_card(row):
    st.markdown(
        f"""
        <div class="card">
          <div class="line"><b>{row['code']} {row['name']}</b><span>{row['pool']}｜LIA {row['lia']}｜MFS {row['mfs']}</span></div>
          <div class="line muted"><span>RS {row['research_score']}｜Confidence {row['confidence']}｜Risk {row['risk_level']}</span><span>{row['action']}</span></div>
          <div class="muted">证据：{row['evidence_summary']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home():
    st.set_page_config(page_title="LJC Capital AI Pro V3.1 RC", page_icon="🚀", layout="wide")
    compact_style()

    os = V31DecisionOS()
    report = os.run_daily()

    st.markdown("### 🚀 LJC Capital AI Pro V3.1 RC")
    st.caption("Execution Edition｜War Room｜Research Watch｜Main Force Tracking")

    st.markdown("#### 🧠 War Room")
    wr = report["war_room"]
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("市场", wr["market_state"])
        c2.metric("仓位", wr["position"])
        c3.metric("主线", wr["theme"])
        c4.metric("风险", wr["risk"])
        st.caption(wr["mission"])

    st.markdown("#### ⭐ Priority Watch")
    for row in report["priority_watch"]:
        render_stock_card(row)

    st.markdown("#### 💎 Diamond Core")
    for row in report["diamond_core"]:
        render_stock_card(row)

    st.markdown("#### 🚀 Opportunity Pool")
    for row in report["opportunity_pool"]:
        render_stock_card(row)

    st.markdown("#### 📊 主力资金纵向跟踪")
    with st.container(border=True):
        for item in report["main_force_summary"]:
            st.caption(item)

    st.markdown("#### 📌 今日执行")
    with st.container(border=True):
        for m in report["execution_missions"]:
            st.write(m)

    st.markdown("#### ⚠ Review / Tomorrow")
    with st.container(border=True):
        st.caption(report["review_summary"])
