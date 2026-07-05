import pandas as pd
from core.pro_v20.decision.decision_center import ProDecisionCenter

class TradePlanEngine:
    def __init__(self):
        self.decision = ProDecisionCenter()

    def plans(self):
        df = self.decision.decisions()
        if df.empty:
            return df

        df = df.copy()
        for c in ["price", "change_pct", "LJC Alpha Score", "risk"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        df["第一买点"] = (df["price"] * 0.985).round(2)
        df["第二买点"] = (df["price"] * 0.965).round(2)
        df["突破买点"] = (df["price"] * 1.025).round(2)
        df["止损"] = (df["price"] * 0.93).round(2)
        df["目标一"] = (df["price"] * 1.10).round(2)
        df["目标二"] = (df["price"] * 1.20).round(2)
        df["目标三"] = (df["price"] * 1.35).round(2)

        df["交易动作"] = "观察"
        df.loc[(df["LJC Alpha Score"] >= 88) & (df["risk"] <= 60), "交易动作"] = "买入/加仓"
        df.loc[(df["LJC Alpha Score"] >= 75) & (df["risk"] <= 70), "交易动作"] = "低吸观察"
        df.loc[(df["risk"] >= 75) | (df["change_pct"] <= -5), "交易动作"] = "减仓/止损"

        df["红绿灯"] = "🟡"
        df.loc[df["交易动作"] == "买入/加仓", "红绿灯"] = "🟢"
        df.loc[df["交易动作"] == "减仓/止损", "红绿灯"] = "🔴"

        cols = ["code","name","price","change_pct","LJC Alpha Score","正式建议","正式仓位","交易动作","红绿灯","第一买点","第二买点","突破买点","止损","目标一","目标二","目标三","证据"]
        return df[[c for c in cols if c in df.columns]].sort_values("LJC Alpha Score", ascending=False)
