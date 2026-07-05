import pandas as pd
from core.factors.base import Factor

class TrendFactor(Factor):
    name = "trend"
    weight = 0.25

    def compute(self, df):
        x = pd.to_numeric(df.get("change_pct", 0), errors="coerce").fillna(0)
        return (50 + x.clip(-10, 10) * 5).clip(0, 100)
