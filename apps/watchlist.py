import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st
from core.watchlist_center import WatchlistCenter

st.set_page_config(page_title="LJC V8.5 自选股中心", page_icon="⭐", layout="wide")
st.title("⭐ LJC V8.5 自选股中心")
st.caption("新增 / 删除 / 编辑 / 保存，数据写入 data/watchlist/watchlist.csv")

wc = WatchlistCenter()

with st.sidebar:
    st.subheader("新增股票")
    code = st.text_input("股票代码", placeholder="例如 300059")
    name = st.text_input("股票名称", placeholder="例如 东方财富")
    note = st.text_input("备注", placeholder="核心观察")
    if st.button("加入自选股", use_container_width=True):
        if code.strip():
            wc.add(code, name, note)
            st.success("已加入")
            st.rerun()
        else:
            st.warning("请输入股票代码")

    st.markdown("---")
    st.subheader("删除股票")
    current = wc.list()
    options = [f"{r.code} {r.name}" for r in current.itertuples()]
    selected = st.selectbox("选择要删除的股票", options=[""] + options)
    if st.button("删除选中股票", use_container_width=True):
        if selected:
            wc.remove(selected.split()[0])
            st.warning(f"已删除：{selected}")
            st.rerun()

tabs = st.tabs(["自选股分析", "编辑保存", "文件位置"])

with tabs[0]:
    df = wc.analyze()
    if df.empty:
        st.warning("暂无自选股")
    else:
        cols = [c for c in ["code","name","note","自选状态","V8动作","买入优先级","V8综合分","首次建仓","最大允许仓位","第一买点","第二买点","止损价","第一止盈","第二止盈","执行结论"] if c in df.columns]
        st.dataframe(df[cols] if cols else df, use_container_width=True, hide_index=True)

with tabs[1]:
    st.info("可以直接编辑表格。删除某行：点行左侧，按 Delete；或用左侧删除框。")
    edited = st.data_editor(
        wc.list(),
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "code": st.column_config.TextColumn("股票代码"),
            "name": st.column_config.TextColumn("股票名称"),
            "note": st.column_config.TextColumn("备注"),
        },
    )
    c1, c2 = st.columns(2)
    if c1.button("保存表格", type="primary", use_container_width=True):
        wc.save(edited)
        st.success("已保存")
        st.rerun()
    if c2.button("清空自选股", use_container_width=True):
        wc.save(pd.DataFrame(columns=["code", "name", "note"]))
        st.warning("已清空")
        st.rerun()

with tabs[2]:
    st.code(str(wc.path))
    st.caption("CSV 列：code,name,note")
