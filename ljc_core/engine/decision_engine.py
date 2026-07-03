from ljc_core.engine.data_engine import DataEngine
from ljc_core.engine.analysis_engine import AnalysisEngine


class DecisionEngine:
    def __init__(self):
        self.data = DataEngine()
        self.analysis = AnalysisEngine()

    def run(self):
        watch = self.data.watchlist()
        mf_df = self.data.main_force()
        daily = self.data.stock_daily()
        portfolio = self.data.portfolio()

        rows = []
        for _, s in watch.iterrows():
            mf = self.analysis.main_force_summary(s["code"], mf_df)
            base = float(s.get("base_lia",80))
            risk = float(s.get("risk",35))
            lia, confidence, pool, action, priority = self.analysis.pool_decision(base, risk, mf)
            if mf["capital_state"] == "资金转弱":
                action, priority = "降级观察/不加仓", "C"

            pr = daily[daily["code"] == s["code"]]
            close = "-" if pr.empty else pr.iloc[-1]["close"]
            chg = "-" if pr.empty else pr.iloc[-1]["change_pct"]

            pos = portfolio[portfolio["code"] == s["code"]]
            cost = "-" if pos.empty else pos.iloc[-1].get("cost","-")
            shares = "-" if pos.empty else pos.iloc[-1].get("shares","-")
            target_weight = "-" if pos.empty else pos.iloc[-1].get("target_weight","-")
            pnl = "-"
            try:
                if cost != "-" and close != "-":
                    pnl = round((float(close)-float(cost))/float(cost)*100, 2)
            except Exception:
                pass

            rows.append({**dict(s), **mf, "lia":lia, "confidence":confidence, "pool":pool, "action":action,
                         "priority":priority, "close":close, "change_pct":chg, "cost":cost, "shares":shares,
                         "target_weight":target_weight, "pnl_pct":pnl,
                         "evidence":f"{mf['capital_state']}；5日主力 {mf['mf_5d']} 亿；风险 {risk}；数据 {mf['latest_date']}"})

        rows = sorted(rows, key=lambda x:(x["priority"]=="S", x["lia"]), reverse=True)
        diamond = [r for r in rows if r["pool"]=="Diamond Core"]
        opportunity = [r for r in rows if r["pool"]=="Opportunity"]
        watch_rows = [r for r in rows if r["pool"]=="Watch"]
        alerts = [f"🟢 {r['name']}：主力资金连续增强，Capital Health {r['capital_health']}" for r in rows if r["capital_health"]>=90]
        alerts += [f"🔴 {r['name']}：资金转弱，进入降级观察" for r in rows if r["capital_state"]=="资金转弱"]
        avg_conf = round(sum(r["confidence"] for r in rows)/max(len(rows),1),1)
        buy = opportunity[0]["name"] if opportunity else "暂无"
        t = diamond[0]["name"] if diamond else "暂无"
        return {
            "war_room":{"market":"机构主线","position":"75%" if avg_conf>=86 else "60%","theme":"商业航天 / AI基础设施",
                        "confidence":avg_conf,"mission":f"重点关注 {buy}；做T候选 {t}；资金转弱股票不加仓。"},
            "diamond":diamond,"opportunity":opportunity,"watch":watch_rows,"alerts":alerts or ["暂无重大预警"],
            "rows":rows,"data_status":self.data.status()
        }
