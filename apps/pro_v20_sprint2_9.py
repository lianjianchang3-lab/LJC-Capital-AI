import sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd

from core.pro_v20.decision import ProDecisionCenter
from core.pro_v20.trading import TradePlanEngine
from core.pro_v20.scanner import MarketScanner
from core.pro_v20.alerts import AlertCenter
from core.pro_v20.review import ReviewCenter
from core.pro_v20.report import MorningReport
from core.pro_v20.portfolio.portfolio_center import ProPortfolioCenter
from core.pro_v20.watchlist.watchlist_center import ProWatchlistCenter

st.set_page_config(page_title="LJC Pro V2.0 Sprint2-9", page_icon="🧠", layout="wide")
st.title("🧠 LJC Capital AI Pro V2.0 Sprint 2-9")
st.caption("AI交易计划｜买卖点｜资金共振｜扫描｜预警｜复盘｜晨报")

auto = st.sidebar.checkbox("自动刷新", True)
sec = st.sidebar.slider("刷新秒数", 10, 120, 30)
top = st.sidebar.slider("显示前N", 6, 100, 30)

tabs = st.tabs(["AI作战首页","交易计划","我的持仓","自选股","市场扫描","预警中心","晨报","复盘","手机部署"])

with tabs[0]:
    brief = ProDecisionCenter().morning_brief()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("AI均分", brief.get("market_score"))
    c2.metric("市场状态", brief.get("market_mode"))
    c3.metric("建议仓位", brief.get("position"))
    c4.metric("买入关注", brief.get("buy_count"))
    st.success(brief.get("summary"))
    st.subheader("今日作战")
    st.dataframe(TradePlanEngine().plans().head(top), use_container_width=True, hide_index=True)

with tabs[1]:
    st.dataframe(TradePlanEngine().plans().head(top), use_container_width=True, hide_index=True)

with tabs[2]:
    p = ProPortfolioCenter().analyze()
    st.success(p.get("summary"))
    st.metric("建议现金", p.get("cash_suggestion"))
    st.dataframe(pd.DataFrame(p.get("holdings",[])), use_container_width=True, hide_index=True)

with tabs[3]:
    st.dataframe(ProWatchlistCenter().analyze().head(top), use_container_width=True, hide_index=True)

with tabs[4]:
    sc = MarketScanner()
    st.subheader("Top候选")
    st.dataframe(sc.scan(top).head(top), use_container_width=True, hide_index=True)
    st.subheader("板块热度")
    st.dataframe(sc.hot_sectors(), use_container_width=True, hide_index=True)

with tabs[5]:
    alerts = AlertCenter().save()
    if alerts:
        for a in alerts[:20]:
            if a["level"] == "RISK":
                st.error(f"{a['code']} {a['name']}｜{a['alert']}｜{a['reason']}")
            elif a["level"] == "HIGH":
                st.success(f"{a['code']} {a['name']}｜{a['alert']}｜{a['reason']}")
            else:
                st.info(f"{a['code']} {a['name']}｜{a['alert']}｜{a['reason']}")
    else:
        st.info("暂无预警")

with tabs[6]:
    text = MorningReport().generate_text()
    st.markdown(text)

with tabs[7]:
    rc = ReviewCenter()
    if st.button("记录当前AI建议"):
        st.dataframe(rc.snapshot(), use_container_width=True, hide_index=True)
    st.json(rc.summary())

with tabs[8]:
    st.code("python -m streamlit run apps/pro_v20_mobile_pro.py --server.address 0.0.0.0 --server.port 8501")

if auto:
    time.sleep(sec)
    st.rerun()
