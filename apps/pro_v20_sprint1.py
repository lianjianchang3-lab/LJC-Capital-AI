import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from core.pro_v20 import ProConfigCenter, ProDecisionCenter, ProWatchlistCenter, ProPortfolioCenter

st.set_page_config(page_title="LJC Pro V2.0 Sprint1", page_icon="🚀", layout="wide")
st.title("🚀 LJC Capital AI Pro V2.0 Sprint 1")
st.caption("AI决策首页｜我的持仓｜自选股作战中心｜今日策略｜配置化")

auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N", 6, 100, 30)

tabs = st.tabs(["今日策略", "自选股作战中心", "我的持仓", "全部AI决策", "配置中心", "手机部署"])

with tabs[0]:
    brief = ProDecisionCenter().morning_brief()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("AI均分", brief.get("market_score"))
    c2.metric("市场状态", brief.get("market_mode"))
    c3.metric("建议仓位", brief.get("position"))
    c4.metric("买入关注", brief.get("buy_count"))
    st.success(brief.get("summary"))
    st.subheader("今日重点")
    st.dataframe(pd.DataFrame(brief.get("top",[])).head(top), use_container_width=True, hide_index=True)

with tabs[1]:
    df = ProWatchlistCenter().analyze()
    st.subheader("重点观察池")
    st.dataframe(df.head(top), use_container_width=True, hide_index=True)

with tabs[2]:
    p = ProPortfolioCenter().analyze()
    st.success(p.get("summary"))
    st.metric("建议现金", p.get("cash_suggestion"))
    st.dataframe(pd.DataFrame(p.get("holdings",[])), use_container_width=True, hide_index=True)
    st.info("请编辑 data/portfolio/holdings.csv 填入成本和股数。")

with tabs[3]:
    df = ProDecisionCenter().decisions()
    st.dataframe(df.head(top), use_container_width=True, hide_index=True)

with tabs[4]:
    cfg = ProConfigCenter()
    st.subheader("自选股配置：config/ljc_watchlist.csv")
    st.dataframe(cfg.watchlist(), use_container_width=True, hide_index=True)
    st.subheader("持仓配置：data/portfolio/holdings.csv")
    st.dataframe(cfg.holdings(), use_container_width=True, hide_index=True)
    st.subheader("评分权重：config/ljc_weights.csv")
    st.json(cfg.weights())

with tabs[5]:
    st.code("python -m streamlit run apps/pro_v20_mobile.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
