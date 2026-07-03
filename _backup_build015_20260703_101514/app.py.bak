try:
    from ljc_core.dashboard.home import render_home
    render_home()
except Exception as e:
    import streamlit as st
    st.error("V4.0 启动失败，已保留旧版 app.py 备份。")
    st.exception(e)
