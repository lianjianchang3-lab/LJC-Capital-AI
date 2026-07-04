from core.v83.score_v4 import AIScoreV4

class PortfolioManagerPro:
    """
    Build341-380: Portfolio Manager Pro
    自动仓位、调仓、止盈止损、资金分配。
    """
    def __init__(self, capital=1000000):
        self.capital = capital

    def plan(self):
        df = AIScoreV4().table()
        if df.empty:
            return {"status": "NO DATA", "capital": self.capital, "cash": self.capital, "positions": []}

        positions = []
        used_weight = 0.0
        for _, r in df.iterrows():
            decision = r.get("ai_decision_v4")
            score = float(r.get("ai_score_v4", 0))
            price = float(r.get("price", 0) or 0)

            if decision == "BUY":
                weight = 0.12
            elif decision == "WATCH_BUY":
                weight = 0.06
            else:
                continue

            if used_weight + weight > 0.55:
                break
            used_weight += weight

            positions.append({
                "code": r.get("code"),
                "name": r.get("name"),
                "decision": decision,
                "target_weight": round(weight, 2),
                "target_amount": round(self.capital * weight, 2),
                "entry_price": round(price * 0.98, 2) if price else None,
                "add_price": round(price * 0.95, 2) if price else None,
                "stop_loss": round(price * 0.92, 2) if price else None,
                "take_profit_1": round(price * 1.12, 2) if price else None,
                "take_profit_2": round(price * 1.22, 2) if price else None,
                "ai_score_v4": score,
                "reason": r.get("explain_v4"),
            })

        cash_weight = round(1 - used_weight, 2)
        return {
            "status": "OK",
            "capital": self.capital,
            "total_position_weight": round(used_weight, 2),
            "cash_weight": cash_weight,
            "cash_amount": round(self.capital * cash_weight, 2),
            "risk_budget": "总仓位≤55%，单股≤12%，CSV/非实时模式保持保守。",
            "positions": positions,
        }
