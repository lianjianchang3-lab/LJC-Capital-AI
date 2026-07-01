import streamlit as st


def render_home():
    st.set_page_config(
        page_title="LCRI Alpha Build005",
        page_icon="🚀",
        layout="wide"
    )

    st.title("🚀 LCRI Alpha Build005")
    st.caption("LJC Capital AI Pro | Mobile First Investment Command Center")

    st.divider()

    st.subheader("🧠 AI Commander")
    st.success("今日策略：保持主线仓位，重点关注商业航天与AI基础设施。允许轻仓做T，严禁追高。")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("建议仓位", "80%")
    c2.metric("今日做T", "YES")
    c3.metric("市场状态", "Main Wave")
    c4.metric("风险等级", "LOW")

    st.divider()

    st.subheader("⭐ LCRI Core")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("LCRI Score", "92.8")
    c2.metric("Diamond", "S")
    c3.metric("Signal", "★★★★★")
    c4.metric("Confidence", "91%")

    st.divider()

    st.subheader("🔥 Diamond Watchlist")
    st.table({
        "股票": ["信维通信", "上海瀚讯", "应流股份"],
        "评级": ["Diamond S", "Diamond A", "Diamond A"],
        "Signal": ["★★★★★", "★★★★☆", "★★★★☆"],
        "操作": ["持有/做T", "观察加仓", "继续持有"]
    })

    st.divider()

    st.subheader("📊 Portfolio")
    c1, c2, c3 = st.columns(3)
    c1.metric("组合仓位", "80%")
    c2.metric("现金比例", "20%")
    c3.metric("组合风险", "LOW")

    st.info("组合建议：继续保持商业航天主线，控制单股仓位，不做满仓。")

    st.divider()

    st.subheader("⚠ Risk Radar")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("市场风险", "LOW")
    c2.metric("行业风险", "MEDIUM")
    c3.metric("个股风险", "LOW")
    c4.metric("执行纪律", "STRICT")

    st.warning("风险提醒：若高位放量分化，降低机动仓；若跌破关键支撑，重新评估。")

    st.divider()

    st.subheader("🎯 今日操作")
    st.write("1. 不追高。")
    st.write("2. 主线回踩可低吸。")
    st.write("3. 信维通信允许轻仓做T。")
    st.write("4. 上海瀚讯等待资金确认。")
    st.write("5. 应流股份继续观察主升确认。")