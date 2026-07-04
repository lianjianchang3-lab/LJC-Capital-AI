from core.market_intel import MarketIntelligence

class MarketRegimeEngine:
    def __init__(self, market=None):
        self.market = market or MarketIntelligence()

    def detect(self):
        m = self.market.snapshot()
        if m.get("status") != "OK":
            return {"status": "NO DATA", "regime": "UNKNOWN", "position": "0%-30%"}
        avg = m.get("avg_lia", 0)
        strong = m.get("strong_count", 0)
        if avg >= 82 and strong >= 3:
            regime = "主升浪 / Risk ON"
            position = "75%-90%"
        elif avg >= 70:
            regime = "结构性机会"
            position = "50%-70%"
        elif avg >= 60:
            regime = "震荡防守"
            position = "30%-50%"
        else:
            regime = "Risk OFF"
            position = "0%-30%"
        return {"status": "OK", "regime": regime, "suggested_position": position, "market": m}
