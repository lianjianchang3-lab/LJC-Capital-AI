import pandas as pd
from core.pro_v20.config.config_center import ProConfigCenter
from core.pro_v20.decision.decision_center import ProDecisionCenter

class ProPortfolioCenter:
    def __init__(self):
        self.config = ProConfigCenter()
        self.decision = ProDecisionCenter()

    def analyze(self):
        holdings = self.config.holdings()
        dec = self.decision.decisions()
        if holdings.empty:
            return {"status":"NO HOLDINGS","summary":"尚未录入持仓","holdings":[],"cash_suggestion":"保守"}

        if not dec.empty and "code" in dec.columns:
            dec["code"] = dec["code"].astype(str).str.zfill(6)
            df = holdings.merge(dec, on="code", how="left", suffixes=("_holding",""))
        else:
            df = holdings.copy()

        for c in ["cost", "shares", "price", "target_weight", "LJC Alpha Score"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        df["市值"] = (df["price"] * df["shares"]).round(2)
        df["成本金额"] = (df["cost"] * df["shares"]).round(2)
        df["浮盈亏"] = (df["市值"] - df["成本金额"]).round(2)
        df["浮盈亏%"] = df.apply(lambda r: round((r["price"]-r["cost"])/r["cost"]*100,2) if r["cost"]>0 else 0, axis=1)

        total_value = float(df["市值"].sum())
        if total_value > 0:
            df["当前仓位占比"] = (df["市值"] / total_value).round(4)
        else:
            df["当前仓位占比"] = 0

        df["持仓建议"] = "观察"
        df.loc[(df["LJC Alpha Score"] >= 85) & (df["浮盈亏%"] > -5), "持仓建议"] = "继续持有/可加仓"
        df.loc[(df["LJC Alpha Score"] < 60) | (df["浮盈亏%"] <= -8), "持仓建议"] = "减仓/检查风险"

        avg_alpha = round(float(df["LJC Alpha Score"].mean()),1) if len(df)>0 else 0
        cash = "35%-45%" if avg_alpha >= 75 else "50%-70%"
        return {
            "status":"OK",
            "summary": f"持仓{len(df)}只，平均Alpha {avg_alpha}，建议现金 {cash}",
            "cash_suggestion": cash,
            "holdings": df.to_dict("records"),
        }
