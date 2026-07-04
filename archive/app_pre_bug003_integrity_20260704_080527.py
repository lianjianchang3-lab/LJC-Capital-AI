import streamlit as st
import pandas as pd

from core import LJCAppCore
from core.gateway import DataGateway
from core.ai import V8FinalAI
from core.health import HealthCheck
from core.status import DataStatusCenter, DataRefreshGuard
from core.data_import import InboxImporter, TemplateManager

st.set_page_config(page_title="LJC Capital AI Pro V8 FINAL", page_icon="🚀", layout="wide")

core = LJCAppCore()
boot = core.boot()
gateway = DataGateway()
ai = V8FinalAI(gateway)
health = HealthCheck().run()
data_status = DataStatusCenter().status()
refresh_guard = DataRefreshGuard()
refresh_status = refresh_guard.all_status()
war = ai.war_room()
signals = ai.signals()
importer = InboxImporter()
templates = TemplateManager()

st.title("🚀 LJC Capital AI Pro V8.0 FINAL RC")

st.markdown("### 📡 Data Status Center")
ds1, ds2, ds3, ds4, ds5 = st.columns(5)
ds1.metric("Mode", data_status["mode"])
ds2.metric("Source", data_status["source"])
ds3.metric("Data Date", data_status["data_date"])
ds4.metric("Updated", data_status["updated_at"])
ds5.metric("Realtime", "ON" if data_status["realtime"] else "OFF")

if data_status["stale"] or not data_status["realtime"]:
    st.error("⚠ 当前为 CSV 本地数据 / 非实时行情。数据可能不是今日行情，禁止直接作为实盘交易依据。")
else:
    st.success("✅ 当前为实时数据模式。")

if data_status["issues"]:
    st.caption(" | ".join(data_status["issues"]))

if refresh_status["needs_update"]:
    st.warning("📥 数据需要更新：请把最新 quotes/capital CSV 放入 data/inbox，然后点击 数据导入 → 导入 inbox CSV。")
    with st.expander("查看CSV文件状态"):
        st.dataframe(pd.DataFrame(refresh_status["files"]), use_container_width=True, hide_index=True)


st.caption("Release Stabilization｜Data Gateway｜AI统一数据流｜手机/电脑一致")

if health["score"] < 90:
    st.warning(f"系统健康度 {health['score']}｜问题：{', '.join(health['issues']) or '无'}")

tabs = st.tabs(["War Room", "Diamond", "Opportunity", "Watch", "Portfolio", "Data Gateway", "数据导入", "Health"])

with tabs[0]:
    st.header("War Room")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("市场", war["market"])
    c2.metric("建议仓位", war["position"])
    c3.metric("Health", data_status["health"])
    c4.metric("Version", boot["version"])

    rows = [{
        "代码": s.code, "名称": s.name, "实时价": s.price, "涨跌幅": s.change_pct,
        "LIA": s.lia, "资金": s.capital_score, "风险": s.risk_score,
        "评级": s.rank, "建议": s.action, "原因": s.reason
    } for s in war["top"]]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

with tabs[1]:
    st.header("💎 Diamond")
    ds = war["diamond"]
    if not ds:
        st.info("暂无 Diamond。")
    for s in ds:
        with st.container(border=True):
            st.markdown(f"### {s.code} {s.name}｜LIA {s.lia}")
            a,b,c,d = st.columns(4)
            a.metric("实时价", s.price)
            b.metric("涨跌幅", f"{s.change_pct}%")
            c.metric("资金", s.capital_score)
            d.metric("风险", s.risk_score)
            st.success(s.action)
            st.caption(s.reason)

with tabs[2]:
    st.header("🚀 Opportunity")
    st.dataframe(pd.DataFrame([s.__dict__ for s in war["opportunity"]]), use_container_width=True, hide_index=True)

with tabs[3]:
    st.header("👀 Watch")
    st.dataframe(pd.DataFrame([s.__dict__ for s in war["watch"]]), use_container_width=True, hide_index=True)

with tabs[4]:
    st.header("Portfolio")
    pf = gateway.portfolio()
    if pf.empty:
        st.info("暂无持仓数据。可在 data/inbox 放入持仓 CSV 后导入。")
    else:
        st.dataframe(pf, use_container_width=True)

with tabs[5]:
    st.header("Data Gateway")
    st.subheader("Quotes")
    st.dataframe(pd.DataFrame([q.__dict__ for q in gateway.quotes()]), use_container_width=True, hide_index=True)
    st.subheader("Capital")
    st.dataframe(pd.DataFrame([c.__dict__ for c in gateway.capital()]), use_container_width=True, hide_index=True)

with tabs[6]:
    st.header("真实数据导入")
    st.code("data/inbox/")
    st.subheader("CSV 文件状态")
    st.dataframe(pd.DataFrame(refresh_status["files"]), use_container_width=True, hide_index=True)
    if refresh_status["inbox_files"]:
        st.success("待导入文件：" + ", ".join(refresh_status["inbox_files"]))
    else:
        st.info("data/inbox 当前没有待导入 CSV。可双击 scripts/open_data_inbox.command 打开文件夹。")
    names = templates.list_templates()
    if names:
        name = st.selectbox("复制模板到 inbox", names)
        if st.button("复制模板"):
            st.write(templates.copy_template_to_inbox(name))
    if st.button("导入 inbox CSV"):
        st.write(importer.import_all())
        st.success("导入完成，请刷新页面。")

with tabs[7]:
    st.header("Health")
    h1, h2, h3, h4 = st.columns(4)
    h1.metric("System Health", data_status["health"])
    h2.metric("Realtime", "ON" if data_status["realtime"] else "OFF")
    h3.metric("Provider", data_status["provider"])
    h4.metric("Freshness", data_status["freshness"])
    st.subheader("Data Status")
    st.json(data_status)
    st.subheader("Data Refresh Guard")
    st.json(refresh_status)
    st.subheader("Gateway Health")
    st.json(health)

st.divider()
st.write("V8.0 FINAL RC：新功能冻结。当前补丁完成 Data Gateway 与稳定入口。")
