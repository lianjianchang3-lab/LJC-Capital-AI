from core.intelligence import InstitutionIntelligenceCore

class MarketIntelligence:
    def __init__(self, core=None):
        self.core = core or InstitutionIntelligenceCore()

    def snapshot(self):
        df = self.core.score()
        if df.empty:
            return {"status": "NO DATA"}
        avg_lia = round(df["lia"].mean(), 1)
        strong = int((df["lia"] >= 80).sum())
        weak = int((df["lia"] < 60).sum())
        if avg_lia >= 80:
            regime = "Risk ON"
        elif avg_lia >= 68:
            regime = "结构性机会"
        else:
            regime = "Risk OFF"
        return {"status": "OK", "regime": regime, "avg_lia": avg_lia, "strong_count": strong, "weak_count": weak, "breadth": f"{strong}/{len(df)}"}
