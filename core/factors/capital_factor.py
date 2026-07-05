import pandas as pd
from core.factors.base import Factor

class CapitalFactor(Factor):
    name = "capital"
    weight = 0.30

    def compute(self, df):
        amount = pd.to_numeric(df.get("amount", 0), errors="coerce").fillna(0)
        vol = pd.to_numeric(df.get("volume", 0), errors="coerce").fillna(0)
        score = amount.rank(pct=True).fillna(0) * 70 + vol.rank(pct=True).fillna(0) * 30
        return score.clip(0, 100)
