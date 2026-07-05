import pandas as pd
from core.factors.base import Factor

class RiskFactor(Factor):
    name = "risk"
    weight = 0.20

    def compute(self, df):
        if "risk" in df.columns:
            risk = pd.to_numeric(df.get("risk", 0), errors="coerce").fillna(0)
            return (100 - risk).clip(0, 100)
        chg = pd.to_numeric(df.get("change_pct", 0), errors="coerce").fillna(0)
        penalty = chg.apply(lambda x: 35 if x <= -5 else 15 if x < 0 else 0)
        return (85 - penalty).clip(0, 100)
