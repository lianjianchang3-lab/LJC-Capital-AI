from core.strategy_v3 import EntryExitEngine

class AlertCenter:
    def __init__(self):
        self.entry_exit = EntryExitEngine()

    def scan(self):
        alerts = []
        for p in self.entry_exit.plans():
            score = p.get("investment_score", 0) or 0
            risk = p.get("risk", 0) or 0
            if p.get("decision") == "WATCH_BUY":
                alerts.append({"level": "INFO", "code": p.get("code"), "name": p.get("name"), "message": "接近观察买点，等待确认"})
            if risk >= 75:
                alerts.append({"level": "RISK", "code": p.get("code"), "name": p.get("name"), "message": "风险偏高，建议检查仓位"})
            if score >= 85:
                alerts.append({"level": "FOCUS", "code": p.get("code"), "name": p.get("name"), "message": "高评分重点关注"})
        return {"alert_count": len(alerts), "alerts": alerts}
