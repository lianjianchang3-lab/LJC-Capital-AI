import pandas as pd
from pathlib import Path

class PortfolioCenterV3:
    def __init__(self):
        self.holdings_path = Path("data/portfolio/holdings.csv")

    def _decision(self):
        try:
            from core.pro_v20.tradeplan.trade_planner_v2 import TradePlannerV2
            df = TradePlannerV2().plan()
            if df is not None and not df.empty:
                df["code"] = df["code"].astype(str).str.zfill(6)
                return df
        except Exception:
            pass
        try:
            from core.pro_v20.decision.decision_center import ProDecisionCenter
            df = ProDecisionCenter().decisions()
            if df is not None and not df.empty:
                df["code"] = df["code"].astype(str).str.zfill(6)
                return df
        except Exception:
            pass
        return pd.DataFrame()

    def _holdings(self):
        if self.holdings_path.exists():
            df = pd.read_csv(self.holdings_path, dtype={"code": str})
        else:
            df = pd.DataFrame([
                {"code":"300136","name":"信维通信","cost":0,"shares":0,"target_weight":0.15},
                {"code":"300762","name":"上海瀚讯","cost":0,"shares":0,"target_weight":0.12},
                {"code":"603308","name":"应流股份","cost":0,"shares":0,"target_weight":0.10},
                {"code":"688008","name":"澜起科技","cost":0,"shares":0,"target_weight":0.12},
                {"code":"688387","name":"信科移动","cost":0,"shares":0,"target_weight":0.08},
                {"code":"300059","name":"东方财富","cost":0,"shares":0,"target_weight":0.08},
            ])
            self.holdings_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(self.holdings_path, index=False)
        df["code"] = df["code"].astype(str).str.zfill(6)
        for c in ["cost","shares","target_weight"]:
            df[c] = pd.to_numeric(df.get(c, 0), errors="coerce").fillna(0)
        return df

    def analyze(self):
        h = self._holdings()
        d = self._decision()
        if d.empty:
            h["状态"] = "暂无行情"
            return {"status":"NO DATA","summary":"暂无AI行情数据","table":h,"total":{}}

        keep = [c for c in d.columns if c not in ["name"]]
        df = h.merge(d[keep], on="code", how="left")
        for c in ["price","cost","shares","target_weight","Alpha2.0","资金共振","综合风险"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        df["市值"] = (df["price"] * df["shares"]).round(2)
        df["成本金额"] = (df["cost"] * df["shares"]).round(2)
        df["浮盈亏"] = (df["市值"] - df["成本金额"]).round(2)
        df["浮盈亏%"] = df.apply(lambda r: round((r["price"]-r["cost"])/r["cost"]*100,2) if r["cost"]>0 else 0, axis=1)
        total_mv = float(df["市值"].sum())
        df["当前仓位占比"] = df["市值"].apply(lambda x: round(x/total_mv,4) if total_mv>0 else 0)

        df["持仓动作"] = "观察"
        df.loc[(df["Alpha2.0"]>=82)&(df["综合风险"]<55), "持仓动作"] = "继续持有/可加仓"
        df.loc[(df["Alpha2.0"]<60)|(df["综合风险"]>=70)|(df["浮盈亏%"]<=-8), "持仓动作"] = "减仓/检查风险"
        df.loc[df["shares"]<=0, "持仓动作"] = df.get("最终动作","观察")

        invested_names = df[df["shares"]>0]["name"].tolist()
        avg_alpha = round(float(df["Alpha2.0"].mean()),1) if len(df)>0 else 0
        avg_risk = round(float(df["综合风险"].mean()),1) if "综合风险" in df else 0

        total = {
            "持仓只数": int((df["shares"]>0).sum()),
            "观察只数": int((df["shares"]<=0).sum()),
            "股票市值": round(total_mv,2),
            "平均Alpha": avg_alpha,
            "平均风险": avg_risk,
            "持仓股票": "、".join(invested_names) if invested_names else "尚未录入实际持仓",
            "建议现金": "40%-60%" if avg_alpha>=70 else "60%-80%",
        }
        summary = f"持仓{total['持仓只数']}只，平均Alpha {avg_alpha}，平均风险 {avg_risk}，建议现金 {total['建议现金']}"
        return {"status":"OK","summary":summary,"table":df,"total":total}
