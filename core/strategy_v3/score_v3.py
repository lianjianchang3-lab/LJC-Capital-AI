from core.intelligence import InstitutionIntelligenceCore

class ScoreV3:
    def __init__(self):
        self.core = InstitutionIntelligenceCore()

    def table(self):
        df = self.core.score()
        if df.empty:
            return df
        df = df.copy()
        df["alpha"] = (df["lia"] * 0.6 + df["trend"] * 0.4).round(1)
        df["beta_risk"] = df["risk"].round(1)
        df["growth"] = (df["trend"] * 0.5 + df["quality"] * 0.5).round(1)
        df["safety"] = (100 - df["risk"]).round(1)
        df["investment_score"] = (df["alpha"]*0.35 + df["capital"]*0.25 + df["growth"]*0.20 + df["safety"]*0.20).round(1)
        return df.sort_values("investment_score", ascending=False)
