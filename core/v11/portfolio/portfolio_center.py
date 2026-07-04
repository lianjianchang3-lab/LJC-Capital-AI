from core.v11.ai.ai_center import AICenterV11
from core.v11.risk.risk_center import RiskCenterV11

class PortfolioCenterV11:
    def plan(self):
        ai = AICenterV11().decisions()
        risk = RiskCenterV11().assess()
        items = ai.get("items", [])
        buy = [x for x in items if x.get("AI决策") in ["重点买入关注","买入观察"]]
        watch = [x for x in items if x.get("AI决策")=="观察"]
        portfolio_risk = risk.get("portfolio_risk")
        if portfolio_risk == "高":
            cash = 0.70
        elif len(buy) >= 3:
            cash = 0.35
        elif len(buy) >= 1:
            cash = 0.50
        else:
            cash = 0.75
        return {"status":"OK","cash_weight":cash,"buy_count":len(buy),"watch_count":len(watch),"risk":portfolio_risk,"summary":f"建议现金{cash:.0%}，买入关注{len(buy)}只，组合风险{portfolio_risk}。","top":buy[:10]}
