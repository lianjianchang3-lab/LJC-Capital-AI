from core.v83.alpha import AlphaValidationCenter
from core.v83.data import V83ProviderManager

class PortfolioAI:
    """
    M4 Portfolio AI.
    根据 Alpha Cards 给出目标组合和现金比例。
    """
    def __init__(self, capital=1000000):
        self.capital = capital
        self.provider = V83ProviderManager()

    def propose(self):
        cards = AlphaValidationCenter().validate().get("cards", [])
        buy = [c for c in cards if c.get("suggestion") == "BUY/HOLD"]
        watch = [c for c in cards if c.get("suggestion") == "WATCH"]
        allocations = []
        remaining = 1.0
        for c in buy[:5]:
            weight = 0.12 if c.get("confidence") in ["A+","A"] else 0.08
            weight = min(weight, remaining)
            remaining -= weight
            allocations.append({
                "code": c["code"],
                "name": c["name"],
                "target_weight": round(weight, 2),
                "target_amount": round(self.capital * weight, 2),
                "reason": c["why"],
            })
        cash = max(0, remaining)
        return {
            "capital": self.capital,
            "cash_weight": round(cash, 2),
            "cash_amount": round(self.capital * cash, 2),
            "allocations": allocations,
            "watch_count": len(watch),
            "risk_budget": "单股≤12%，CSV模式下建议保守执行。",
        }
