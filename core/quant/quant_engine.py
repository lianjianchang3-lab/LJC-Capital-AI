from core.strategy_v3 import ScoreV3

class QuantEngine:
    def factors(self):
        df = ScoreV3().table()
        if df.empty:
            return df
        out = df.copy()
        out["momentum_factor"] = out["trend"]
        out["capital_factor"] = out["capital"]
        out["risk_factor"] = 100 - out["risk"]
        out["quality_factor"] = out["quality"]
        out["quant_score"] = (
            out["momentum_factor"]*0.30 +
            out["capital_factor"]*0.30 +
            out["risk_factor"]*0.20 +
            out["quality_factor"]*0.20
        ).round(1)
        return out.sort_values("quant_score", ascending=False)
