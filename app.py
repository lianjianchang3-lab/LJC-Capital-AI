import streamlit as st
from core import LJCAppCore
from core.data_center import DataCenter

core = LJCAppCore()
boot = core.boot()
dc = DataCenter()
health = dc.health_check()

st.set_page_config(page_title="LJC Capital AI Pro V8", page_icon="🚀", layout="wide")

st.title("🚀 LJC Capital AI Pro V8.0")
st.caption("Build002 Data Center MVP｜统一数据入口")

with st.container(border=True):
    st.subheader("System Status")
    st.write("App:", boot["app"].get("name", "LJC Capital AI Pro"))
    st.write("Version:", boot["version"])
    st.write("Data Center Quality:", health["overall_score"])

st.subheader("Data Center")
c1, c2, c3, c4, c5 = st.columns(5)
for col, key in zip([c1, c2, c3, c4, c5], ["watchlist", "quotes", "capital", "sector", "news"]):
    q = health["checks"][key]
    col.metric(key, q.score, q.status)

watch = dc.get_watchlist().data
quotes = dc.get_quotes().data
capital = dc.get_capital().data
sector = dc.get_sector().data

st.subheader("Watchlist")
st.dataframe(watch, use_container_width=True)

st.subheader("Quotes")
st.dataframe(quotes, use_container_width=True)

st.subheader("Capital")
st.dataframe(capital, use_container_width=True)

st.subheader("Sector")
st.dataframe(sector, use_container_width=True)

st.subheader("V8.0 Progress")
st.progress(0.20)
st.write("Build002 Data Center MVP: 已安装")
st.write("下一步：Build003 Capital Engine")
