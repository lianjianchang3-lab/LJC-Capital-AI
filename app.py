import streamlit as st
from core import LJCAppCore

core = LJCAppCore()
boot = core.boot()

st.set_page_config(page_title="LJC Capital AI Pro V8", page_icon="🚀", layout="wide")

st.title("🚀 LJC Capital AI Pro V8.0")
st.caption("Build001 Foundation｜Core / Config / Logger / Version / Plugin")

with st.container(border=True):
    st.subheader("System Status")
    st.write("App:", boot["app"].get("name", "LJC Capital AI Pro"))
    st.write("Version:", boot["version"])
    st.write("Plugins:", boot["plugins"])

st.subheader("V8.0 Progress")
st.progress(0.10)
st.write("Build001 Foundation: 已安装")
st.write("下一步：Build002 Data Center MVP")
