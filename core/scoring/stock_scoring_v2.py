from core.intelligence import InstitutionIntelligenceCore

class StockScoringV2:
    def __init__(self, core=None):
        self.core = core or InstitutionIntelligenceCore()

    def score(self):
        df = self.core.score()
        if df.empty:
            return df
        out = df.copy()
        out["theme"] = 70
        out["fundamental"] = 65
        out["score2"] = (
            out["lia"] * 0.45 +
            out["capital"] * 0.20 +
            out["trend"] * 0.15 +
            (100 - out["risk"]) * 0.10 +
            out["theme"] * 0.05 +
            out["fundamental"] * 0.05
        ).round(1)
        def grade(x):
            if x >= 88: return "S"
            if x >= 80: return "A"
            if x >= 70: return "B"
            if x >= 60: return "C"
            return "D"
        out["grade2"] = out["score2"].apply(grade)
        return out.sort_values("score2", ascending=False)
