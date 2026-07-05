import pandas as pd
from core.decision import DecisionCore

class InstitutionEngine:
    def __init__(self):
        self.decision = DecisionCore()

    def run(self):
        df = self.decision.trade_plan()
        if df is None or df.empty:
            return pd.DataFrame()

        df = df.copy()
        for c in ["amount", "volume", "change_pct", "LCRI Score", "capital_score", "trend_score", "risk_score"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        df["机构成交强度"] = (
            df["amount"].rank(pct=True).fillna(0) * 100 * 0.65
            + df["volume"].rank(pct=True).fillna(0) * 100 * 0.35
        ).round(1)

        df["北向模拟分"] = (
            df["trend_score"] * 0.45
            + df["capital_score"] * 0.35
            + df["change_pct"].clip(-10, 10) * 2
            + 10
        ).clip(0, 100).round(1)

        df["龙虎榜模拟分"] = (
            df["capital_score"] * 0.50
            + df["机构成交强度"] * 0.30
            + df["LCRI Score"] * 0.20
        ).clip(0, 100).round(1)

        df["基金关注分"] = (
            df["LCRI Score"] * 0.50
            + df["risk_score"] * 0.25
            + df["trend_score"] * 0.25
        ).clip(0, 100).round(1)

        df["机构共振指数"] = (
            df["北向模拟分"] * 0.25
            + df["龙虎榜模拟分"] * 0.30
            + df["基金关注分"] * 0.25
            + df["机构成交强度"] * 0.20
        ).round(1)

        df["机构评级"] = "BB"
        df.loc[df["机构共振指数"] >= 60, "机构评级"] = "A"
        df.loc[df["机构共振指数"] >= 75, "机构评级"] = "AA"
        df.loc[df["机构共振指数"] >= 88, "机构评级"] = "AAA"

        df["机构动作"] = "观察"
        df.loc[(df["机构共振指数"] >= 75) & (df["LCRI Score"] >= 75), "机构动作"] = "机构关注"
        df.loc[(df["机构共振指数"] >= 88) & (df["LCRI Score"] >= 82), "机构动作"] = "机构共振"
        df.loc[(df["机构共振指数"] < 45) | (df["LCRI Score"] < 50), "机构动作"] = "机构回避"

        df["机构证据"] = df.apply(
            lambda r: f"机构共振={r['机构共振指数']} 北向={r['北向模拟分']} 龙虎={r['龙虎榜模拟分']} 基金={r['基金关注分']} 成交={r['机构成交强度']}",
            axis=1
        )
        return df.sort_values(["机构共振指数", "LCRI Score"], ascending=False)
