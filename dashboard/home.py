import streamlit as st


def render_home():
    st.set_page_config(
        page_title="LCRI Alpha",
        page_icon="🚀",
        layout="wide"
    )

    st.title("🚀 LCRI Alpha")
    st.caption("LJC Capital Research Intelligence｜Mobile First Investment OS")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Global Capital", "82")
    col2.metric("Industry Heat", "79")
    col3.metric("Main Wave", "86")
    col4.metric("Risk", "LOW")

    st.divider()

    st.subheader("🌍 Global Scan")
    st.info("全球风险偏好维持积极，AI基础设施与商业航天继续获得资金关注。")

    st.subheader("🧭 Strategy")
    st.markdown("""
1. AI基础设施 ⭐⭐⭐⭐⭐  
2. 商业航天 ⭐⭐⭐⭐⭐  
3. 空天地一体化 ⭐⭐⭐⭐☆
""")

    st.subheader("🚀 Action Pool")
    st.table({
        "股票": ["信维通信", "应流股份", "上海瀚讯"],
        "评级": ["WATCH", "WATCH", "OBSERVE"]
    })

    st.subheader("📈 Main Wave Radar")
    st.progress(0.86, text="主升浪概率：86%")

    st.subheader("⚠ Risk Radar")
    st.warning("关注成交量变化、高位板块分化和追高风险。")

    st.subheader("🎯 Nova Action")
    st.success("保持耐心，不追高，重点关注一级股票池。")