try:
    from dashboard_v32.home import render_home
    render_home()
except Exception as e:
    import streamlit as st
    st.error("V3.2 启动失败，已保留旧版 app.py 备份。")
    st.exception(e)
