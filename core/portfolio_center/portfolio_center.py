from pathlib import Path
import pandas as pd


class PortfolioCenter:
    """
    V8.5 Build002 持仓中心。
    读取 data/portfolio/holdings.csv，并与 ExecutionCenter 的最新建议合并。
    holdings.csv 支持列：
    code,name,shares,cost
    """

    def __init__(self, holdings_path="data/portfolio/holdings.csv"):
        self.holdings_path = Path(holdings_path)

    def _sample_if_missing(self):
        self.holdings_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.holdings_path.exists():
            pd.DataFrame([
                {"code": "300059", "name": "东方财富", "shares": 0, "cost": 0},
                {"code": "688387", "name": "信科移动", "shares": 0, "cost": 0},
            ]).to_csv(self.holdings_path, index=False)

    def holdings(self):
        self._sample_if_missing()
        try:
            df = pd.read_csv(self.holdings_path, dtype={"code": str})
        except Exception:
            return pd.DataFrame()
        if df.empty:
            return df
        df["code"] = df["code"].astype(str).str.replace(".0", "", regex=False).str.zfill(6)
        for c in ["shares", "cost"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        if "name" not in df.columns:
            df["name"] = df["code"]
        return df

    def analyze(self):
        h = self.holdings()
        if h.empty:
            return pd.DataFrame()

        from core.execution import ExecutionCenter
        exe = ExecutionCenter().dataframe()
        if exe is None or exe.empty:
            return h

        exe = exe.copy()
        exe["code"] = exe["code"].astype(str).str.zfill(6)
        keep = [c for c in [
            "code","price","V8动作","V8综合分","买入优先级","首次建仓","最大允许仓位",
            "风险预算","第一买点","第二买点","突破确认价","止损价","第一止盈","第二止盈","执行结论"
        ] if c in exe.columns]
        df = h.merge(exe[keep], on="code", how="left")

        for c in ["price", "cost", "shares"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        df["市值"] = (df["price"] * df["shares"]).round(2)
        df["成本市值"] = (df["cost"] * df["shares"]).round(2)
        df["浮盈浮亏"] = ((df["price"] - df["cost"]) * df["shares"]).round(2)
        df["浮盈浮亏%"] = df.apply(lambda r: round((r["price"] - r["cost"]) / r["cost"] * 100, 2) if r["cost"] > 0 else 0, axis=1)

        df["持仓建议"] = "观察"
        df.loc[df["shares"] <= 0, "持仓建议"] = "未持有"
        df.loc[(df["shares"] > 0) & (df["V8动作"].astype(str).str.contains("回避", na=False)), "持仓建议"] = "减仓/回避"
        df.loc[(df["shares"] > 0) & (df["price"] > 0) & (df["price"] <= df["止损价"]), "持仓建议"] = "触发止损"
        df.loc[(df["shares"] > 0) & (df["price"] >= df["第一止盈"]) & (df["第一止盈"] > 0), "持仓建议"] = "达到止盈区"
        df.loc[(df["shares"] > 0) & (df["买入优先级"] <= 3) & (df["风险预算"].isin(["低","中"])), "持仓建议"] = "可继续持有"

        df["组合操作"] = df.apply(self._operation, axis=1)
        return df.sort_values(["持仓建议","V8综合分"], ascending=[True, False])

    def _operation(self, r):
        if r.get("shares", 0) <= 0:
            return "未持有，按执行中心观察"
        sug = str(r.get("持仓建议", "观察"))
        if "止损" in sug:
            return "严格执行止损纪律"
        if "止盈" in sug:
            return "分批止盈，保留底仓观察"
        if "减仓" in sug:
            return "优先减仓或清仓"
        if "继续持有" in sug:
            return "继续持有，跌破止损减仓"
        return "观察，不主动加仓"

    def summary(self):
        df = self.analyze()
        if df.empty:
            return {"status": "NO DATA", "summary": "暂无持仓"}
        total = round(float(df["市值"].sum()), 2) if "市值" in df.columns else 0
        pnl = round(float(df["浮盈浮亏"].sum()), 2) if "浮盈浮亏" in df.columns else 0
        risk_count = int(df["持仓建议"].astype(str).str.contains("止损|减仓|回避", na=False).sum())
        return {
            "status": "OK",
            "total_value": total,
            "pnl": pnl,
            "risk_count": risk_count,
            "summary": f"持仓市值 {total}，浮盈浮亏 {pnl}，风险持仓 {risk_count} 只。"
        }
