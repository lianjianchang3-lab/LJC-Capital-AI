import pandas as pd
from core.factors.base import Factor

class VolumeFactor(Factor):
    name = "volume"
    weight = 0.15

    def compute(self, df):
        vol = pd.to_numeric(df.get("volume", 0), errors="coerce").fillna(0)
        return (vol.rank(pct=True).fillna(0) * 100).clip(0, 100)
