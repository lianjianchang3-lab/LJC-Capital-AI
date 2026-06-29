import streamlit as st
from src.data.datasource import DataSource
from analysis.scanner_engine import ScannerEngine
from analysis.decision_engine import DecisionEngine


st.set_page_config(
    page_title="LJC Capital AI Professional",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 LJC Capital AI Professional V7.0")
st.caption("Build 0.4 | 统一数据模型 + AI个股分析中心")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("系统状态", "正常")
with col2:
    st.metric("数据源", "AkShare")
with col3:
    st.metric("当前版本", "V7.0 Build 0.4")
with col4:
    st.metric("核心模型", "StockAnalysisResult")

st.divider()

st.header("🚀 今日 Top20 爆发榜")

sort_type = st.selectbox("排序方式", ["AI评分", "涨跌幅", "成交额"])

if st.button("开始扫描全部A股"):
    with st.spinner("正在扫描全市场，请稍等..."):
        ds = DataSource()
        stock_list = ds.get_stock_list()
        scanner = ScannerEngine(stock_list)
        top20 = scanner.scan_top20()

        if sort_type in top20.columns:
            top20 = top20.sort_values(by=sort_type, ascending=False)

    st.success("扫描完成")
    st.dataframe(top20, width="stretch")

st.divider()

st.header("🔍 AI 个股分析中心")

code = st.text_input("输入股票代码，例如 300136", value="300136")

if st.button("开始AI分析"):
    ds = DataSource()
    name = ds.get_stock_name(code)
    df = ds.get_daily_data(code)

    st.subheader(f"{code} {name}")

    if df.empty:
        st.error("没有读取到数据")
    else:
        result = DecisionEngine(code, name, df).calculate()

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            st.metric("AI评分", result.ai_score)
        with c2:
            st.metric("BEI爆发指数", result.bei)
        with c3:
            st.metric("CRI资金共振", result.cri)
        with c4:
            st.metric("ICI机构信心", result.ici)
        with c5:
            st.metric("RRI风险收益", result.rri)

        st.success(f"AI建议：{result.recommendation}")

        col_a, col_b = st.columns(2)

        with col_a:
            st.metric("目标价", result.target_price)
        with col_b:
            st.metric("止损位", result.stop_loss)

        st.markdown("### 证据链")
        for item in result.evidence:
            st.write("✅", item)

        st.markdown("### 最近5日行情")
        st.dataframe(df.tail(), width="stretch")

st.divider()

st.header("⭐ 我的观察池")

watchlist = [
    {"股票": "信维通信", "代码": "300136", "状态": "重点跟踪"},
    {"股票": "上海瀚讯", "代码": "300762", "状态": "重点跟踪"},
    {"股票": "应流股份", "代码": "603308", "状态": "重点跟踪"},
    {"股票": "英诺激光", "代码": "301021", "状态": "观察"},
]

st.dataframe(watchlist, width="stretch")

st.divider()

st.header("💼 多账户管理")

accounts = [
    {"账户": "A股主账户", "资金": "100万", "风格": "激进成长", "仓位": "待接入", "状态": "启用"},
    {"账户": "家庭账户", "资金": "60万", "风格": "稳健", "仓位": "待接入", "状态": "启用"},
    {"账户": "模拟账户", "资金": "20万", "风格": "测试", "仓位": "待接入", "状态": "启用"},
]

st.dataframe(accounts, width="stretch")

st.divider()

st.warning("提示：本系统为投资分析辅助工具，不构成任何买卖承诺。")