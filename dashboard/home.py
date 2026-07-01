import streamlit as st
import pandas as pd


DIAMOND_UNIVERSE = [
    {"代码": "300136", "股票": "信维通信", "分层": "Core", "LCRI": 96, "Diamond": "S", "Signal": "★★★★★", "操作": "持有/做T"},
    {"代码": "300762", "股票": "上海瀚讯", "分层": "Priority", "LCRI": 94, "Diamond": "A", "Signal": "★★★★☆", "操作": "分批买入"},
    {"代码": "603308", "股票": "应流股份", "分层": "Priority", "LCRI": 93, "Diamond": "A", "Signal": "★★★★☆", "操作": "继续持有"},
    {"代码": "688008", "股票": "澜起科技", "分层": "Priority", "LCRI": 92, "Diamond": "A", "Signal": "★★★★☆", "操作": "等待低吸"},
    {"代码": "688387", "股票": "信科移动", "分层": "Priority", "LCRI": 91, "Diamond": "A", "Signal": "★★★★☆", "操作": "观察资金"},
    {"代码": "300342", "股票": "天银机电", "分层": "Watch", "LCRI": 88, "Diamond": "B", "Signal": "★★★☆☆", "操作": "观察"},
    {"代码": "688568", "股票": "中科星图", "分层": "Watch", "LCRI": 87, "Diamond": "B", "Signal": "★★★☆☆", "操作": "观察"},
    {"代码": "600879", "股票": "航天电子", "分层": "Watch", "LCRI": 84, "Diamond": "Watch", "Signal": "★★★☆☆", "操作": "等待"},
    {"代码": "600391", "股票": "航发科技", "分层": "Watch", "LCRI": 83, "Diamond": "Watch", "Signal": "★★★☆☆", "操作": "等待"},
    {"代码": "301021", "股票": "英诺激光", "分层": "Watch", "LCRI": 82, "Diamond": "Watch", "Signal": "★★★☆☆", "操作": "等待"},
    {"代码": "300058", "股票": "蓝色光标", "分层": "Watch", "LCRI": 81, "Diamond": "Watch", "Signal": "★★★☆☆", "操作": "等待"},
    {"代码": "000426", "股票": "兴业银锡", "分层": "Watch", "LCRI": 80, "Diamond": "Watch", "Signal": "★★★☆☆", "操作": "等待"},
    {"代码": "600301", "股票": "华锡有色", "分层": "Watch", "LCRI": 79, "Diamond": "Watch", "Signal": "★★★☆☆", "操作": "等待"},
]


def render_home():
    st.set_page_config(
        page_title="LJC Capital AI Pro Build006",
        page_icon="🚀",
        layout="wide",
    )

    st.title("🚀 LJC Capital AI Pro Build006")
    st.caption("Diamond Universe | Mobile First Command Center")

    st.divider()

    st.subheader("🧠 AI Commander")
    st.success("今日策略：保持80%仓位，核心持有信维通信，重点关注上海瀚讯、应流股份、澜起科技。允许轻仓做T，不追高。")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("建议仓位", "80%")
    c2.metric("今日做T", "YES")
    c3.metric("市场状态", "主升浪")
    c4.metric("风险等级", "LOW")

    st.divider()

    st.subheader("💎 Diamond Universe（13只）")

    df = pd.DataFrame(DIAMOND_UNIVERSE).sort_values("LCRI", ascending=False)
    st.dataframe(df, width="stretch", hide_index=True)

    st.divider()

    st.subheader("🔥 今日任务")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ 继续持有")
        st.write("300136 信维通信")
        st.write("603308 应流股份")

        st.markdown("### 🟢 可重点关注")
        st.write("300762 上海瀚讯")
        st.write("688008 澜起科技")

    with col2:
        st.markdown("### 🔄 今日可做T")
        st.write("300136 信维通信")

        st.markdown("### ⚠ 暂不追高")
        st.write("300342 天银机电")
        st.write("688568 中科星图")
        st.write("600879 航天电子")

    st.divider()

    st.subheader("⭐ LCRI 总览")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("最高LCRI", "96")
    c2.metric("Diamond A以上", "5")
    c3.metric("可执行标的", "4")
    c4.metric("观察标的", "8")

    st.divider()

    st.subheader("⚠ Risk Radar")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("市场风险", "LOW")
    c2.metric("行业风险", "MEDIUM")
    c3.metric("个股风险", "LOW")
    c4.metric("执行纪律", "STRICT")

    st.warning("纪律：不追高；低吸优先；跌破关键支撑重新评估；单股不超过25%。")