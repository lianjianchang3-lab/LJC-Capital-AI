import pandas as pd
from core.pro_v20.alpha.alpha_engine_v2 import AlphaEngineV2

class CapitalEngineV2:
    def __init__(self):
        self.alpha = AlphaEngineV2()

    def run(self):
        df = self.alpha.run()
        if df is None or df.empty:
            return pd.DataFrame()
        df = df.copy()
        for c in ["amount","volume","change_pct","资金分","量能分","main_inflow"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        df["主力模拟分"] = (df["资金分"]*0.55 + df["量能分"]*0.30 + df["change_pct"].clip(-10,10)*1.5 + 20).clip(0,100).round(1)
        df["资金共振"] = (df["主力模拟分"]*0.5 + df["资金分"]*0.3 + df["量能分"]*0.2).round(1)

        df["资金状态"] = "普通"
        df.loc[df["资金共振"]>=70, "资金状态"] = "资金活跃"
        df.loc[df["资金共振"]>=85, "资金状态"] = "资金共振"
        df.loc[df["change_pct"]<0, "资金状态"] = "分歧观察"

        return df.sort_values("资金共振", ascending=False)
