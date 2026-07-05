import pandas as pd
from core.pro_v20.decision.decision_center import ProDecisionCenter

class MarketScanner:
    def __init__(self):
        self.decision = ProDecisionCenter()

    def scan(self, top_n=20):
        df = self.decision.decisions()
        if df.empty:
            return df

        df = df.copy()
        for c in ["LJC Alpha Score","change_pct","risk","amount","volume"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        df["扫描标签"] = "普通观察"
        df.loc[(df["LJC Alpha Score"]>=85)&(df["risk"]<=65), "扫描标签"] = "今日强势候选"
        df.loc[(df["change_pct"]>=5)&(df["amount"].rank(pct=True)>=0.6), "扫描标签"] = "资金异动"
        df.loc[(df["risk"]>=75)|(df["change_pct"]<=-5), "扫描标签"] = "风险过滤"

        return df.sort_values(["LJC Alpha Score","amount"], ascending=False).head(top_n)

    def hot_sectors(self):
        df = self.decision.decisions()
        if df.empty or "sector" not in df.columns:
            return pd.DataFrame()
        x = df.groupby("sector").agg(
            股票数=("code","count"),
            平均Alpha=("LJC Alpha Score","mean"),
            平均涨幅=("change_pct","mean")
        ).reset_index()
        x["平均Alpha"] = x["平均Alpha"].round(1)
        x["平均涨幅"] = x["平均涨幅"].round(2)
        return x.sort_values("平均Alpha", ascending=False)
