import streamlit as st
import pandas as pd

from core import LJCAppCore
from core.data_center import DataCenter
from core.lia import LIAEngine
from core.decision import DecisionEngine
from core.portfolio import PortfolioEngine
from core.data_import import InboxImporter, TemplateManager
from core.morning import MorningBrief
from core.health import HealthCheck
from updater import UpdateService

core = LJCAppCore()
boot = core.boot()
dc = DataCenter()
lia_engine = LIAEngine(dc)
decision_engine = DecisionEngine(lia_engine)
portfolio_engine = PortfolioEngine(lia_engine=lia_engine)
brief = MorningBrief(decision_engine)
updater = UpdateService()
importer = InboxImporter()
templates = TemplateManager()
health = HealthCheck().run()

morning = brief.generate()
signals = decision_engine.make_plan().get("signals", [])

st.set_page_config(page_title="LJC Capital AI Pro V8", page_icon="🚀", layout="wide")

st.title("🚀 LJC Capital AI Pro V8.0")
st.caption("RC4｜Morning Brief｜真实数据｜健康检查｜一键启动")

if health["score"] < 90:
    st.warning(f"系统健康度 {health['score']}，建议进入「系统检查」查看。")

tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "晨会首页", "今日决策", "LIA排行", "我的持仓", "真实数据导入", "更新中心", "系统检查"
])

with tab0:
    st.header("☀️ LJC Morning Brief")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("市场状态", morning["market"])
    c2.metric("建议仓位", morning["position"])
    c3.metric("风险", morning["risk"])
    c4.metric("系统健康", health["score"])

    st.info(morning["summary"])

    st.subheader("💎 Diamond")
    if morning["diamond"]:
        for s in morning["diamond"]:
            with st.container(border=True):
                st.markdown(f"### {s.code} {s.name}｜LIA {s.lia}")
                a, b, c, d = st.columns(4)
                a.metric("资金", s.capital)
                b.metric("趋势", s.trend)
                c.metric("板块", s.sector)
                d.metric("可信度", s.confidence)
                st.write(s.action)
                st.caption(s.explanation)
    else:
        st.write("暂无 Diamond。")

    st.subheader("🚀 Opportunity")
    if morning["opportunity"]:
        for s in morning["opportunity"]:
            st.write(f"{s.code} {s.name}｜LIA {s.lia}｜{s.action}")
    else:
        st.write("暂无 Opportunity。")

    st.subheader("⚠️ 今日纪律")
    st.write("不追高；优先看资金连续性；真实数据导入后再做最终判断。")

with tab1:
    plan = decision_engine.make_plan()
    st.subheader("今日作战计划")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("市场", plan["market"])
    c2.metric("仓位", plan["position"])
    c3.metric("风险", plan["risk"])
    c4.metric("版本", boot["version"])
    st.write(plan["summary"])

with tab2:
    rows = [{
        "代码": s.code,
        "名称": s.name,
        "LIA": s.lia,
        "资金": s.capital,
        "趋势": s.trend,
        "板块": s.sector,
        "风险安全": s.risk,
        "可信度": s.confidence,
        "评级": s.rank,
        "建议": s.action,
        "说明": s.explanation,
    } for s in signals]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

with tab3:
    st.dataframe(portfolio_engine.analyze(), use_container_width=True, hide_index=True)
    st.caption("真实持仓可放入 data/inbox/，文件名包含 portfolio 或 持仓。")

with tab4:
    st.subheader("真实数据导入")
    st.write("把同花顺 / Moomoo / 东方财富 / 持仓 CSV 放入：")
    st.code("data/inbox/")

    st.markdown("#### CSV 模板")
    names = templates.list_templates()
    if names:
        selected_template = st.selectbox("选择模板复制到 inbox", names)
        if st.button("复制模板到 inbox"):
            st.write(templates.copy_template_to_inbox(selected_template))
    else:
        st.warning("未找到模板文件。")

    st.markdown("#### 导入")
    if st.button("导入 inbox CSV 并刷新数据"):
        result = importer.import_all()
        st.write(result)
        st.success("导入完成。请刷新页面查看最新分析。")

with tab5:
    st.subheader("更新中心")
    st.write(updater.check())
    st.code("桌面快捷方式：LJC Update.command")
    if st.button("手动拉取 develop 更新"):
        st.code(updater.pull())

with tab6:
    st.subheader("系统检查")
    st.metric("Health Score", health["score"])
    st.dataframe(pd.DataFrame(health["results"]), use_container_width=True, hide_index=True)
    st.caption("桌面快捷方式：LJC Health Check.command")

st.divider()
st.progress(0.96)
st.write("V8.0 RC4：系统检查 + 桌面快捷方式完善。")


with tab8:
    st.subheader("Cloud Bridge 云桥同步")
    st.write("状态：", bridge_status["status"])
    st.write("更新时间：", bridge_status["updated_at"])
    st.write(bridge_status["message"])
    if st.button("立即发布到 Cloud Bridge"):
        st.write(bridge.publish())
        st.success("已生成 cloud/live_state.json")
    data = bridge.load()
    if isinstance(data, dict):
        st.caption("云桥数据预览")
        st.json({k: v for k, v in data.items() if k not in ["quotes", "capital", "portfolio"]})
    st.warning("当前为半云端实时：Mac负责采集/发布，手机或云端读取。下一步可接 Supabase/Firebase/S3 等真正云数据库。")
