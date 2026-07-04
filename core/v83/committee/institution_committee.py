from core.v83.alpha import AlphaValidationCenter
from core.v83.learning import LearningEngine
from core.v83.portfolio import PortfolioAI
from core.v83.data import V83ProviderManager

class InstitutionCommittee:
    """
    M5 Institution Committee.
    趋势/资金/量化/风险/组合 五方投票。
    """
    def meeting(self):
        cards = AlphaValidationCenter().validate().get("cards", [])
        portfolio = PortfolioAI().propose()
        model = LearningEngine().latest()
        data = V83ProviderManager().health()

        votes = []
        for c in cards[:10]:
            buy_votes = 0
            if c.get("investment_score",0) >= 80: buy_votes += 1
            if c.get("capital",0) >= 70: buy_votes += 1
            if c.get("risk",100) <= 65: buy_votes += 1
            if c.get("confidence") in ["A+","A"]: buy_votes += 1
            if c.get("lia",0) >= 75: buy_votes += 1
            final = "BUY" if buy_votes >= 4 else "WATCH" if buy_votes >= 2 else "AVOID"
            votes.append({
                "code": c.get("code"),
                "name": c.get("name"),
                "buy_votes": buy_votes,
                "final": final,
                "confidence": c.get("confidence"),
                "why": c.get("why"),
            })

        return {
            "data_health": data,
            "model": model,
            "portfolio": portfolio,
            "votes": votes,
            "final_summary": "优先选择高票数、低风险、高资金评分标的；CSV模式下保持保守仓位。",
        }
