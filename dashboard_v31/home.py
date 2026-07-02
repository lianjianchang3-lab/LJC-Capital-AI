import streamlit as st
from engine_v31.decision_os import V31DecisionOS


def _style():
    st.markdown('''
    <style>
    .block-container {padding-top:.6rem; padding-bottom:.7rem; max-width:980px;}
    h1,h2,h3 {margin-top:.15rem; margin-bottom:.15rem;}
    div[data-testid="stMetricValue"] {font-size:1rem;}
    div[data-testid="stMetricLabel"] {font-size:.68rem;}
    .card {border:1px solid rgba(120,120,120,.25); border-radius:9px; padding:7px 9px; margin:4px 0; font-size:.86rem;}
    .muted {opacity:.72; font-size:.75rem;}
    </style>
    ''', unsafe_allow_html=True)


def render_home():
    st.set_page_config(page_title="LJC Capital AI Pro V3.1", page_icon="🚀", layout="wide")
    _style()

    data = V31DecisionOS().run()
    wr = data["war_room"]

    st.markdown("### 🚀 LJC Capital AI Pro V3.1")
    st.caption("One-Click Incremental Edition｜不覆盖原核心代码")

    st.markdown("#### 🧠 War Room")
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("市场", wr["market"])
        c2.metric("仓位", wr["position"])
        c3.metric("主线", wr["theme"])
        c4.metric("风险", wr["risk"])
        st.caption(wr["mission"])

    def card(row):
        st.markdown(
            f'''<div class="card"><b>{row["code"]} {row["name"]}</b>｜{row["pool"]}｜LIA {row["lia"]}｜MFS {row["mfs"]}<br>
            <span class="muted">动作：{row["action"]}｜证据：{row["evidence"]}</span></div>''',
            unsafe_allow_html=True,
        )

    st.markdown("#### 💎 Diamond Core")
    for r in data["diamond"]:
        card(r)

    st.markdown("#### 🚀 Opportunity Pool")
    for r in data["opportunity"]:
        card(r)

    st.markdown("#### 👀 Watch")
    for r in data["watch"]:
        card(r)

    st.markdown("#### 📊 主力资金纵向跟踪")
    with st.container(border=True):
        for line in data["capital"]:
            st.caption(line)

    st.markdown("#### 📌 今日执行纪律")
    with st.container(border=True):
        st.write("不追高；低吸优先；做T只用机动仓；资金转弱自动降级观察。")
