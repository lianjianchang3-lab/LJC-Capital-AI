from core.provider import ProviderManager
from core.strategy import MasterStrategyEngine
from core.signal import SignalEngine
from core.market_intel import MarketIntelligence
from core.report_center import ReportEngine

class CommercialUIData:
    def __init__(self):
        self.provider = ProviderManager()
        self.master = MasterStrategyEngine()
        self.signal = SignalEngine()
        self.market = MarketIntelligence()
        self.report = ReportEngine()

    def committee_summary(self):
        s = self.master.generate()
        m = s.get("market", {})
        return {
            "market_status": m.get("regime", "UNKNOWN"),
            "suggested_position": s.get("suggested_position", "N/A"),
            "avg_lia": m.get("avg_lia", "N/A"),
            "breadth": m.get("breadth", "N/A"),
            "focus_count": len(s.get("focus", [])),
            "reduce_count": len(s.get("reduce", [])),
            "note": s.get("final_note", ""),
        }

    def score_table(self):
        df = self.signal.signals()
        if df.empty:
            return df
        cols = [c for c in ["code","name","price","change_pct","main_inflow","lia","risk","signal","action","trigger"] if c in df.columns]
        return df[cols]

    def market_temperature(self):
        m = self.market.snapshot()
        avg = m.get("avg_lia", 0)
        try:
            avg_num = float(avg)
        except Exception:
            avg_num = 0
        if avg_num >= 80:
            temp = "Hot"
        elif avg_num >= 68:
            temp = "Warm"
        else:
            temp = "Cold"
        m["temperature"] = temp
        return m

    def position_dashboard(self):
        c = self.committee_summary()
        pos = c.get("suggested_position", "30%-50%")
        return {
            "suggested_position": pos,
            "max_single_stock": "20%",
            "risk_budget": "中低" if str(pos).startswith("30") else "中等",
            "mode": "Defensive" if str(pos).startswith("30") else "Balanced",
        }

    def capital_heatmap(self):
        df = self.signal.signals()
        if df.empty:
            return []
        rows = []
        for _, r in df.iterrows():
            rows.append({
                "code": r.get("code",""),
                "name": r.get("name",""),
                "capital": r.get("capital", r.get("main_inflow", 0)),
                "lia": r.get("lia", 0),
                "signal": r.get("signal",""),
            })
        return rows

    def watchlist(self):
        df = self.signal.signals()
        if df.empty:
            return []
        return df[df["signal"].isin(["BUY/HOLD","WATCH_BUY","WATCH"])].head(10).to_dict("records")

    def risk_center(self):
        df = self.signal.signals()
        if df.empty:
            return {"status": "NO DATA", "risks": []}
        risks = df[df["signal"].isin(["REDUCE","AVOID"])].head(10)
        return {"status": "OK", "risk_count": len(risks), "risks": risks.to_dict("records"), "note": "风险中心基于CSV数据，非实时行情。"}

    def daily_report(self):
        return self.report.daily_brief()
