from core.v90.data import V90RealtimeManager
from core.v83 import InstitutionCommittee, PortfolioAI, AlphaValidationCenter

class V90DecisionEngine:
    def dashboard(self):
        data = V90RealtimeManager()
        health = data.health()
        quotes = data.get_quotes()
        alpha = AlphaValidationCenter().validate()
        portfolio = PortfolioAI().propose()
        committee = InstitutionCommittee().meeting()

        return {
            "version": "V9.0 Stable Candidate",
            "data_health": health,
            "quote_count": len(quotes),
            "alpha_count": len(alpha.get("cards", [])),
            "cash_weight": portfolio.get("cash_weight"),
            "watch_count": portfolio.get("watch_count"),
            "committee_summary": committee.get("final_summary"),
            "votes": committee.get("votes", []),
            "portfolio": portfolio,
            "realtime_note": "如果 active_source = Realtime CSV，说明实时数据层已启用；否则使用备用CSV。",
        }

    def trading_plan(self):
        d = self.dashboard()
        actions = []
        for v in d.get("votes", []):
            final = v.get("final")
            if final == "BUY":
                action = "BUY"
                position = "5%-12%"
            elif final == "WATCH":
                action = "WATCH"
                position = "0%-3%"
            else:
                action = "AVOID"
                position = "0%"
            actions.append({
                "code": v.get("code"),
                "name": v.get("name"),
                "action": action,
                "suggested_position": position,
                "confidence": v.get("confidence"),
                "buy_votes": v.get("buy_votes"),
                "why": v.get("why"),
            })
        return {
            "market_mode": d.get("data_health", {}).get("active_source"),
            "cash_weight": d.get("cash_weight"),
            "actions": actions,
            "risk_note": "研究辅助，不构成自动实盘交易指令；实盘前需人工确认数据和风险。",
        }
