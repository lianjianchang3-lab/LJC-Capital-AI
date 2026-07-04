from core.strategy_v3.score_v3 import ScoreV3

class EntryExitEngine:
    def __init__(self):
        self.score = ScoreV3()

    def plans(self):
        df = self.score.table()
        if df.empty:
            return []
        plans = []
        for _, r in df.iterrows():
            price = float(r.get("price", 0) or 0)
            score = float(r.get("investment_score", 0) or 0)
            risk = float(r.get("beta_risk", 50) or 50)
            if score >= 85 and risk <= 65:
                decision = "BUY/HOLD"
                entry = round(price * 0.98, 2) if price else None
                add = round(price * 0.95, 2) if price else None
            elif score >= 75:
                decision = "WATCH_BUY"
                entry = round(price * 0.96, 2) if price else None
                add = round(price * 0.93, 2) if price else None
            elif risk >= 75:
                decision = "REDUCE"
                entry = None
                add = None
            else:
                decision = "WATCH"
                entry = None
                add = None
            stop = round(price * 0.92, 2) if price else None
            target1 = round(price * 1.12, 2) if price else None
            target2 = round(price * 1.22, 2) if price else None
            plans.append({
                "code": r.get("code", ""),
                "name": r.get("name", ""),
                "price": price,
                "investment_score": score,
                "risk": risk,
                "decision": decision,
                "entry_price": entry,
                "add_price": add,
                "stop_loss": stop,
                "target1": target1,
                "target2": target2,
                "reason": f"Score={score}, Risk={risk}, Capital={r.get('capital')}",
            })
        return plans
