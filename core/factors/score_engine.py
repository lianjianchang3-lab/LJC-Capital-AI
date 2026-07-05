import pandas as pd
from core.factors.trend_factor import TrendFactor
from core.factors.capital_factor import CapitalFactor
from core.factors.volume_factor import VolumeFactor
from core.factors.risk_factor import RiskFactor

class ScoreEngine:
    def __init__(self, factors=None):
        self.factors = factors or [CapitalFactor(), TrendFactor(), VolumeFactor(), RiskFactor()]

    def score(self, df):
        if df is None or df.empty:
            return pd.DataFrame()
        out = df.copy()
        total_weight = sum(f.weight for f in self.factors)
        total = 0
        evidence_cols = []
        for factor in self.factors:
            col = f"{factor.name}_score"
            out[col] = factor.compute(out).round(1)
            total = total + out[col] * factor.weight
            evidence_cols.append(col)
        out["LCRI Score"] = (total / total_weight).round(1)
        out["LCRI Grade"] = "C"
        out.loc[out["LCRI Score"] >= 70, "LCRI Grade"] = "B"
        out.loc[out["LCRI Score"] >= 82, "LCRI Grade"] = "A"
        out.loc[out["LCRI Score"] >= 90, "LCRI Grade"] = "S"
        out["LCRI Evidence"] = out.apply(lambda r: " | ".join([f"{c}={r[c]}" for c in evidence_cols]), axis=1)
        return out.sort_values("LCRI Score", ascending=False)
