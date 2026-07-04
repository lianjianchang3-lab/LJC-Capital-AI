from core.scoring import StockScoringV2
from core.regime import MarketRegimeEngine

class PositionManager:
    def __init__(self, scorer=None, regime=None):
        self.scorer = scorer or StockScoringV2()
        self.regime = regime or MarketRegimeEngine()

    def advise(self):
        df = self.scorer.score()
        reg = self.regime.detect()
        if df.empty:
            return {"status": "NO DATA", "rows": []}
        rows = []
        for _, r in df.iterrows():
            if r["score2"] >= 85 and r["risk"] <= 60:
                pos = "15%-25%"
                action = "核心仓"
            elif r["score2"] >= 75:
                pos = "8%-15%"
                action = "观察仓/低吸"
            elif r["score2"] >= 65:
                pos = "0%-8%"
                action = "轻仓跟踪"
            else:
                pos = "0%"
                action = "不参与/退出"
            rows.append({"code": r["code"], "name": r["name"], "score2": r["score2"], "risk": r["risk"], "suggested_position": pos, "action": action})
        return {"status": "OK", "market_position": reg.get("suggested_position"), "rows": rows}
