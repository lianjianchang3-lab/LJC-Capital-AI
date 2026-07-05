import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

import streamlit as st
from core.daily_plan import DailyPlan

st.set_page_config(page_title="LJC V8.5 Daily", page_icon="📱", layout="centered")
plan = DailyPlan().generate()
market = plan.get("market", {}) or {}

st.title("📱 LJC V8.5 每日计划")
c1,c2 = st.columns(2)
c1.metric("市场", market.get("state","-"))
c2.metric("仓位", plan.get("position","-"))

st.subheader("今日买入/关注")
for r in plan.get("buy", [])[:8]:
    st.success(f"{r.get('code')} {r.get('name')}｜优先级{r.get('买入优先级')}｜首仓{r.get('首次建仓')}｜最大{r.get('最大允许仓位')}")
    st.caption(f"买点 {r.get('第一买点')}/{r.get('第二买点')}｜止损 {r.get('止损价')}")

st.subheader("今日风险/减仓")
items = plan.get("reduce", []) + plan.get("avoid", [])
if not items:
    st.info("暂无明显风险")
for r in items[:8]:
    st.error(f"{r.get('code')} {r.get('name')}｜{r.get('持仓建议') or r.get('V8动作')}｜{r.get('执行结论') or r.get('组合操作')}")
