import streamlit as st
import pandas as pd


STOCKS = [
    ["300136", "信维通信", "Core", 96, "S", "★★★★★", "继续持有 / 做T"],
    ["300762", "上海瀚讯", "Priority", 94, "A", "★★★★☆", "分批买入"],
    ["603308", "应流股份", "Priority", 93, "A", "★★★★☆", "继续持有"],
    ["688008", "澜起科技", "Priority", 92, "A", "★★★★☆", "等待低吸"],
    ["688387", "信科移动", "Priority", 91, "A", "★★★★☆", "观察资金"],
    ["300342", "天银机电", "Watch", 88, "B", "★★★☆☆", "观察"],
    ["688568", "中科星图", "Watch", 87, "B", "★★★☆☆", "观察"],
    ["600879", "航天电子", "Watch", 84, "Watch", "★★★☆☆", "等待"],
    ["600391", "航发科技", "Watch", 83, "Watch", "★★★☆☆", "等待"],
    ["301021", "英诺激光", "Watch", 82, "Watch", "★★★☆☆", "等待"],
    ["300058", "蓝色光标", "Watch", 81, "Watch", "★★★☆☆", "等待"],
    ["000426", "兴业银锡", "Watch", 80, "Watch", "★★★☆☆", "等待"],
    ["600301", "华锡有色", "Watch", 79, "Watch", "★★★☆☆", "等待"],
]


def render_stock_card(code, name, layer, lcri, diamond, signal, action):
    with st.container(border=True):
        st.markdown(f"### 💎 {code} {name}")
        c1, c2, c3 = st.columns(3)
        c1.metric("LCRI", lcri)
        c2.metric("Diamond", diamond)
        c3.metric("Signal", signal)
        st.write(f"**分层：** {layer}")
        st.success(f"建议：{action}")


def render_home():
    st.set_page_config(
        page_title="LJC Capital AI Pro Build006 V2",
        page_icon="🚀",
        layout="wide",
    )

    st.title("🚀 LJC Capital AI Pro Build006 V2")
    st.caption("Diamond Universe V2 | Mobile First Command Center")

    st.divider()

    st.subheader("🧠 Nova Commander")
    with st.container(border=True):
        st.markdown("### 今日行动")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🟢 今日买入")
            st.write("300762 上海瀚讯")
            st.write("688008 澜起科技")

            st.markdown("#### 🔄 今日做T")
            st.write("300136 信维通信")

        with c2:
            st.markdown("#### ✅ 继续持有")
            st.write("300136 信维通信")
            st.write("603308 应流股份")

            st.markdown("#### ⚠ 风险")
            st.write("LOW：可积极观察，但不追高")

    st.divider()

    st.subheader("🥇 Today's Top5")
    top5 = pd.DataFrame(STOCKS, columns=["代码", "股票", "分层", "LCRI", "Diamond", "Signal", "操作"]).head(5)

    for i, row in top5.iterrows():
        medal = ["🥇", "🥈", "🥉", "TOP4", "TOP5"][i]
        with st.container(border=True):
            st.markdown(f"### {medal} {row['代码']} {row['股票']}")
            c1, c2, c3 = st.columns(3)
            c1.metric("LCRI", row["LCRI"])
            c2.metric("Diamond", row["Diamond"])
            c3.metric("Signal", row["Signal"])
            st.success(row["操作"])

    st.divider()

    st.subheader("💎 Diamond Universe Cards")

    for item in STOCKS:
        render_stock_card(*item)

    st.divider()

    st.subheader("📊 Portfolio Commander")
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("信维通信", "25%")
        c2.metric("上海瀚讯", "15%")
        c3.metric("应流股份", "20%")
        c4.metric("现金", "40%")
        st.info("组合建议：保持核心仓位，现金保留40%，等待主线回踩或突破确认。")

    st.divider()

    st.subheader("⚠ Risk Radar")
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("市场风险", "LOW")
        c2.metric("行业风险", "MEDIUM")
        c3.metric("个股风险", "LOW")
        c4.metric("执行纪律", "STRICT")
        st.warning("纪律：不追高；低吸优先；单股不超过25%；做T只用机动仓。")