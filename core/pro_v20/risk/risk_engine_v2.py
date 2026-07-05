import pandas as pd
from core.pro_v20.alpha.alpha_engine_v2 import AlphaEngineV2

class RiskEngineV2:
    def __init__(self):
        self.alpha = AlphaEngineV2()

    def run(self):
        df = self.alpha.run()
        if df is None or df.empty:
            return pd.DataFrame()
        df = df.copy()
        for c in ["risk","change_pct","Alpha2.0","price"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        df["综合风险"] = (df["risk"]*0.60 + (100-df["Alpha2.0"])*0.25 + df["change_pct"].apply(lambda x: 30 if x < -3 else 0)*0.15).clip(0,100).round(1)
        df["风险等级"] = "低"
        df.loc[df["综合风险"]>=45, "风险等级"] = "中"
        df.loc[df["综合风险"]>=70, "风险等级"] = "高"

        df["止损位"] = (df["price"]*0.93).round(2)
        df["第一目标"] = (df["price"]*1.10).round(2)
        df["第二目标"] = (df["price"]*1.20).round(2)

        return df.sort_values("综合风险", ascending=False)
