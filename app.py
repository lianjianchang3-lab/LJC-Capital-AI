import streamlit as st
from src.data.datasource import DataSource
from analysis.scanner_engine import ScannerEngine

st.set_page_config(
    page_title="LJC Capital AI Professional",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 LJC Capital AI Professional V7.0")
st.caption("机构级A股智能分析决策系统 | Scanner + Analyzer + Portfolio")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("系统状态", "正常")
with col2:
    st.metric("数据源", "AkShare")
with col3:
    st.metric("当前版本", "V7.0 Build 0.1")

st.divider()

st.header("🚀 今日Top20爆发榜")

if st.button("开始扫描全部A股"):
    with st.spinner("正在扫描全市场，请稍等..."):
        ds = DataSource()
        stock_list = ds.get_stock_list()
        scanner = ScannerEngine(stock_list)
        top20 = scanner.scan_top20()

    st.success("扫描完成")
    st.dataframe(top20, use_container_width=True)

st.divider()

st.header("🔍 单股分析")

code = st.text_input("输入股票代码，例如 300136", value="300136")

if st.button("开始个股分析"):
    ds = DataSource()
    name = ds.get_stock_name(code)
    df = ds.get_daily_data(code)

    st.subheader(f"{code} {name}")

    if df.empty:
        st.error("没有读取到数据")
    else:
        st.write("最近5日行情")
        st.dataframe(df.tail(), use_container_width=True)

st.divider()

st.header("⭐ 我的观察池")

watchlist = {
    "信维通信": "300136",
    "上海瀚讯": "300762",
    "应流股份": "603308",
    "英诺激光": "301021"
}

st.table(watchlist)

st.divider()

st.header("💼 多账户管理")

accounts = [
    {"账户": "A股主账户", "资金": "100万", "风格": "激进成长", "状态": "启用"},
    {"账户": "家庭账户", "资金": "60万", "风格": "稳健", "状态": "启用"},
    {"账户": "模拟账户", "资金": "20万", "风格": "测试", "状态": "启用"},
]

st.dataframe(accounts, use_container_width=True)

st.divider()

st.warning("提示：本系统为投资分析辅助工具，不构成任何买卖承诺。")