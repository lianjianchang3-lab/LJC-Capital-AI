import pandas as pd
from core.pro_v20.decision.decision_center import ProDecisionCenter

class AlphaEngineV2:
    def __init__(self):
        self.decision = ProDecisionCenter()

    def run(self):
        df = self.decision.decisions()
        if df is None or df.empty:
            return pd.DataFrame()
        df = df.copy()
        for c in ["LJC Alpha Score","资金分","趋势分","量能分","风险分","risk","price","change_pct","amount","volume"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        df["Alpha2.0"] = (
            df["LJC Alpha Score"]*0.35 +
            df["资金分"]*0.20 +
            df["趋势分"]*0.20 +
            df["量能分"]*0.10 +
            df["风险分"]*0.15
        ).round(1)

        df["市场温度"] = (df["趋势分"]*0.5 + df["量能分"]*0.3 + df["资金分"]*0.2).round(1)
        df["胜率估计"] = (45 + df["Alpha2.0"]*0.45 - df["risk"]*0.12).clip(35, 92).round(1)
        df["盈亏比"] = ((df["Alpha2.0"]/50).clip(0.8, 2.5)).round(2)

        df["Alpha等级"] = "C"
        df.loc[df["Alpha2.0"]>=70, "Alpha等级"] = "B"
        df.loc[df["Alpha2.0"]>=82, "Alpha等级"] = "A"
        df.loc[df["Alpha2.0"]>=90, "Alpha等级"] = "S"

        df["最终动作"] = "观察"
        df.loc[(df["Alpha2.0"]>=82)&(df["risk"]<=60), "最终动作"] = "买入关注"
        df.loc[(df["Alpha2.0"]>=70)&(df["risk"]<=70), "最终动作"] = "小仓试探"
        df.loc[(df["risk"]>=75)|(df["change_pct"]<=-5), "最终动作"] = "减仓/回避"

        return df.sort_values("Alpha2.0", ascending=False)
