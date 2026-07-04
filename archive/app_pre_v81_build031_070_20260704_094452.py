from core.workbench import WorkbenchEngine
from core.strategy_v3 import MasterStrategyV3, ScoreV3, EntryExitEngine
from core.selection import SelectionCenter
from core.portfolio_v3 import PortfolioManagerV3
from core.ui import CommercialUIData
import streamlit as st
import pandas as pd

from core import LJCAppCore
from core.gateway import DataGateway
from core.ai import V8FinalAI
from core.health import HealthCheck
from core.status import DataStatusCenter, DataRefreshGuard
from core.validation import DataIntegrityValidator, ReleaseValidationCenter
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
data_integrity = DataIntegrityValidator().validate()
release_validation = ReleaseValidationCenter().validate()
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

tabs = st.tabs(["War Room", "Diamond", "Opportunity", "Watch", "Portfolio", "Data Gateway", "数据导入", "Health", "Release Validation"])

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


with tabs[8]:
    st.header("✅ Release Validation")
    st.metric("Overall", release_validation["overall"])
    st.subheader("Release Checks")
    st.dataframe(pd.DataFrame(release_validation["checks"]), use_container_width=True, hide_index=True)

    st.subheader("Data Integrity")
    st.dataframe(pd.DataFrame(data_integrity["checks"]), use_container_width=True, hide_index=True)

    if release_validation["pass"]:
        st.success("V8.0 FINAL RC 当前通过发布验收。")
    else:
        st.error("V8.0 FINAL RC 尚未通过发布验收，请先修复 FAILED 项。")

# ==============================
# V8.1 Commercial Edition
# Build001-006 Combined
# ==============================
try:
    from core.provider import ProviderManager
    from core.decision import DecisionEngineV2
    from core.portfolio_pro import PortfolioProAnalyzer
    from core.backtest import BacktestEngine
    from core.cloud import CloudSync
    from core.report_center import ReportEngine

    st.divider()
    st.header("🧩 V8.1 Commercial Edition")
    provider_manager_v81 = ProviderManager()
    decision_v2 = DecisionEngineV2(provider_manager_v81)
    portfolio_pro = PortfolioProAnalyzer(provider_manager_v81)
    backtest_engine = BacktestEngine()
    cloud_sync = CloudSync()
    report_engine = ReportEngine()

    v81tabs = st.tabs(["Provider", "Decision V2", "Portfolio Pro", "Backtest", "Cloud Sync", "Report Center"])

    with v81tabs[0]:
        st.subheader("Build001 Provider Framework")
        st.json(provider_manager_v81.health())

    with v81tabs[1]:
        st.subheader("Build002 Decision Engine V2")
        st.dataframe(decision_v2.decisions(), use_container_width=True, hide_index=True)

    with v81tabs[2]:
        st.subheader("Build003 Portfolio Pro")
        result = portfolio_pro.analyze()
        st.json(result["summary"])
        if hasattr(result["positions"], "empty") and not result["positions"].empty:
            st.dataframe(result["positions"], use_container_width=True, hide_index=True)

    with v81tabs[3]:
        st.subheader("Build004 Backtest Center")
        st.json(backtest_engine.run())

    with v81tabs[4]:
        st.subheader("Build005 Cloud Sync")
        st.json(cloud_sync.status())

    with v81tabs[5]:
        st.subheader("Build006 AI Report Center")
        st.json(report_engine.daily_brief())
except Exception as e:
    st.error(f"V8.1 Commercial Edition 加载失败：{e}")

# ==============================
# V8.1 Phase 2 Build007-012
# ==============================
try:
    from core.intelligence import InstitutionIntelligenceCore
    from core.signal import SignalEngine
    from core.portfolio_intel import PortfolioIntelligence
    from core.market_intel import MarketIntelligence
    from core.strategy import MasterStrategyEngine

    st.divider()
    st.header("🧠 V8.1 Phase 2 Strategy Core")
    phase2tabs = st.tabs(["Institution Rating", "Signal Engine", "Portfolio Intelligence", "Market Intelligence", "AI Daily Report 2.0", "Master Strategy"])

    inst_core = InstitutionIntelligenceCore()
    signal_engine = SignalEngine(inst_core)
    portfolio_intel = PortfolioIntelligence()
    market_intel = MarketIntelligence(inst_core)
    master_strategy = MasterStrategyEngine()

    with phase2tabs[0]:
        st.subheader("Build007 Institution Intelligence Core")
        st.dataframe(inst_core.score(), use_container_width=True, hide_index=True)

    with phase2tabs[1]:
        st.subheader("Build008 Signal Engine")
        st.dataframe(signal_engine.signals(), use_container_width=True, hide_index=True)

    with phase2tabs[2]:
        st.subheader("Build009 Portfolio Intelligence")
        st.json(portfolio_intel.analyze())

    with phase2tabs[3]:
        st.subheader("Build010 Market Intelligence")
        st.json(market_intel.snapshot())

    with phase2tabs[4]:
        st.subheader("Build011 AI Daily Report 2.0")
        st.json(report_engine.daily_brief())

    with phase2tabs[5]:
        st.subheader("Build012 Master Strategy Engine")
        st.json(master_strategy.generate())
except Exception as e:
    st.error(f"V8.1 Phase 2 加载失败：{e}")

# ==============================
# V8.1 Phase 2 Build007-012
# ==============================
try:
    from core.intelligence import InstitutionIntelligenceCore
    from core.signal import SignalEngine
    from core.portfolio_intel import PortfolioIntelligence
    from core.market_intel import MarketIntelligence
    from core.strategy import MasterStrategyEngine

    st.divider()
    st.header("🧠 V8.1 Phase 2 Strategy Core")
    phase2tabs = st.tabs(["Institution Rating", "Signal Engine", "Portfolio Intelligence", "Market Intelligence", "AI Daily Report 2.0", "Master Strategy"])

    inst_core = InstitutionIntelligenceCore()
    signal_engine = SignalEngine(inst_core)
    portfolio_intel = PortfolioIntelligence()
    market_intel = MarketIntelligence(inst_core)
    master_strategy = MasterStrategyEngine()

    with phase2tabs[0]:
        st.subheader("Build007 Institution Intelligence Core")
        st.dataframe(inst_core.score(), use_container_width=True, hide_index=True)

    with phase2tabs[1]:
        st.subheader("Build008 Signal Engine")
        st.dataframe(signal_engine.signals(), use_container_width=True, hide_index=True)

    with phase2tabs[2]:
        st.subheader("Build009 Portfolio Intelligence")
        st.json(portfolio_intel.analyze())

    with phase2tabs[3]:
        st.subheader("Build010 Market Intelligence")
        st.json(market_intel.snapshot())

    with phase2tabs[4]:
        st.subheader("Build011 AI Daily Report 2.0")
        st.json(report_engine.daily_brief())

    with phase2tabs[5]:
        st.subheader("Build012 Master Strategy Engine")
        st.json(master_strategy.generate())
except Exception as e:
    st.error(f"V8.1 Phase 2 加载失败：{e}")

# ==============================
# V8.1 Phase 3 Build013-018
# ==============================
try:
    from core.tracker import InstitutionTracker
    from core.regime import MarketRegimeEngine
    from core.scoring import StockScoringV2
    from core.position import PositionManager
    from core.rotation import SectorRotation
    from core.committee import InvestmentCommittee

    st.divider()
    st.header("🏛️ V8.1 Phase 3 Investment Committee")
    phase3tabs = st.tabs(["Institution Tracker", "Market Regime", "Stock Score 2.0", "Position Manager", "Sector Rotation", "Investment Committee"])

    with phase3tabs[0]:
        st.subheader("Build013 Institution Tracker")
        st.json(InstitutionTracker().track())

    with phase3tabs[1]:
        st.subheader("Build014 Market Regime Engine")
        st.json(MarketRegimeEngine().detect())

    with phase3tabs[2]:
        st.subheader("Build015 Stock Scoring 2.0")
        st.dataframe(StockScoringV2().score(), use_container_width=True, hide_index=True)

    with phase3tabs[3]:
        st.subheader("Build016 Position Manager")
        st.json(PositionManager().advise())

    with phase3tabs[4]:
        st.subheader("Build017 Sector Rotation")
        st.json(SectorRotation().analyze())

    with phase3tabs[5]:
        st.subheader("Build018 AI Investment Committee")
        st.json(InvestmentCommittee().run())
except Exception as e:
    st.error(f"V8.1 Phase 3 加载失败：{e}")

# ==============================
# V8.1 Phase 4 Build019-030
# Commercial UI Freeze
# ==============================
try:
    st.divider()
    st.header("🏦 V8.1 Phase 4 Commercial UI")
    ui = CommercialUIData()

    ui_tabs = st.tabs([
        "AI Committee",
        "Stock Score",
        "Market Temperature",
        "Position Dashboard",
        "Capital Heatmap",
        "Institution Rank",
        "Stock Detail",
        "WatchList",
        "Dashboard Pro",
        "Risk Center",
        "AI Daily Report",
        "UI Freeze"
    ])

    with ui_tabs[0]:
        st.subheader("Build019 AI Investment Committee Card")
        c = ui.committee_summary()
        a,b,c1,d = st.columns(4)
        a.metric("市场状态", c["market_status"])
        b.metric("建议仓位", c["suggested_position"])
        c1.metric("平均LIA", c["avg_lia"])
        d.metric("市场宽度", c["breadth"])
        st.info(c["note"])

    with ui_tabs[1]:
        st.subheader("Build020 Stock Score 2.0")
        st.dataframe(ui.score_table(), use_container_width=True, hide_index=True)

    with ui_tabs[2]:
        st.subheader("Build021 Market Temperature")
        m = ui.market_temperature()
        t1,t2,t3,t4 = st.columns(4)
        t1.metric("温度", m.get("temperature"))
        t2.metric("市场", m.get("regime"))
        t3.metric("平均LIA", m.get("avg_lia"))
        t4.metric("强势数", m.get("strong_count"))

    with ui_tabs[3]:
        st.subheader("Build022 Position Dashboard")
        st.json(ui.position_dashboard())

    with ui_tabs[4]:
        st.subheader("Build023 Capital Heatmap")
        st.dataframe(pd.DataFrame(ui.capital_heatmap()), use_container_width=True, hide_index=True)

    with ui_tabs[5]:
        st.subheader("Build024 Institution / Capital Ranking")
        df = ui.score_table()
        if hasattr(df, "empty") and not df.empty:
            st.dataframe(df.sort_values("lia", ascending=False), use_container_width=True, hide_index=True)
        else:
            st.info("暂无排行数据")

    with ui_tabs[6]:
        st.subheader("Build025 Stock Detail")
        df = ui.score_table()
        if hasattr(df, "empty") and not df.empty:
            selected = st.selectbox("选择股票", df["code"].astype(str) + " " + df["name"].astype(str))
            code = selected.split(" ")[0]
            st.json(df[df["code"].astype(str)==code].iloc[0].to_dict())
        else:
            st.info("暂无股票详情")

    with ui_tabs[7]:
        st.subheader("Build026 WatchList")
        st.dataframe(pd.DataFrame(ui.watchlist()), use_container_width=True, hide_index=True)

    with ui_tabs[8]:
        st.subheader("Build027 Dashboard Pro")
        c = ui.committee_summary()
        st.success(f"市场：{c['market_status']}｜建议仓位：{c['suggested_position']}｜平均LIA：{c['avg_lia']}")
        st.dataframe(ui.score_table().head(5), use_container_width=True, hide_index=True)

    with ui_tabs[9]:
        st.subheader("Build028 Risk Center")
        st.json(ui.risk_center())

    with ui_tabs[10]:
        st.subheader("Build029 AI Daily Report")
        st.json(ui.daily_report())

    with ui_tabs[11]:
        st.subheader("Build030 Commercial UI Freeze")
        st.success("V8.1 Commercial UI 已进入冻结候选状态。后续只修 UI Bug，不再增加新页面。")
        st.markdown("""
        - Build019 AI委员会卡片
        - Build020 股票评分表
        - Build021 市场温度
        - Build022 仓位仪表盘
        - Build023 资金热力图
        - Build024 机构资金排行
        - Build025 股票详情
        - Build026 WatchList
        - Build027 Dashboard Pro
        - Build028 风险中心
        - Build029 AI日报
        - Build030 UI Freeze
        """)
except Exception as e:
    st.error(f"V8.1 Phase 4 Commercial UI 加载失败：{e}")

# ==============================
# V8.1 Build031-070 Strategy Workbench
# ==============================
try:
    st.divider()
    st.header("🧭 V8.1 Build031-070 Strategy Workbench")
    wb = WorkbenchEngine()
    master_v3 = MasterStrategyV3()
    score_v3 = ScoreV3()
    entry_exit = EntryExitEngine()
    selection_center = SelectionCenter()
    portfolio_v3 = PortfolioManagerV3()

    btabs = st.tabs(["Master V3", "Entry/Exit", "Score V3", "Selection", "Portfolio V3", "Daily Workbench", "Report Export"])

    with btabs[0]:
        st.subheader("Build031-040 Master Strategy V3")
        st.json(master_v3.generate())

    with btabs[1]:
        st.subheader("Buy/Sell Plan")
        st.dataframe(pd.DataFrame(entry_exit.plans()), use_container_width=True, hide_index=True)

    with btabs[2]:
        st.subheader("AI Investment Score V3")
        st.dataframe(score_v3.table(), use_container_width=True, hide_index=True)

    with btabs[3]:
        st.subheader("Build041-050 Selection Center")
        st.json(selection_center.scan())

    with btabs[4]:
        st.subheader("Build051-060 Portfolio Manager V3")
        st.json(portfolio_v3.analyze())

    with btabs[5]:
        st.subheader("Build061-070 Daily Workbench")
        st.json(wb.daily_plan())

    with btabs[6]:
        st.subheader("Markdown Report")
        st.code(wb.report_markdown(), language="markdown")

except Exception as e:
    st.error(f"V8.1 Build031-070 加载失败：{e}")
