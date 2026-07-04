import pandas as pd
from core.v91.realtime import V91RealtimeHub

class V91AutoScanner:
    """
    自动扫描：
    - 资金流入
    - 涨跌幅
    - 趋势
    - 风险
    - LIA
    """
    def scan(self):
        df = V91RealtimeHub().quotes()
        if df.empty:
            return {"status": "NO DATA", "items": [], "summary": "等待实时数据"}

        df = df.copy()
        for col in ["change_pct","main_inflow","trend","capital","risk","quality","lia"]:
            if col not in df.columns:
                df[col] = 0
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        df["scan_score"] = (
            df["change_pct"].clip(-10, 10) * 2
            + df["main_inflow"] * 12
            + df["trend"] * 0.25
            + df["capital"] * 0.25
            + df["lia"] * 0.20
            - df["risk"] * 0.20
        ).round(1)

        df["signal"] = "WATCH"
        df.loc[(df["scan_score"] >= 75) & (df["risk"] <= 60), "signal"] = "BUY"
        df.loc[(df["risk"] >= 75), "signal"] = "AVOID"
        df.loc[(df["change_pct"] < -4), "signal"] = "RISK_ALERT"

        df = df.sort_values("scan_score", ascending=False)
        strong = int((df["signal"] == "BUY").sum())
        alerts = int((df["signal"].isin(["AVOID","RISK_ALERT"])).sum())
        return {
            "status": "OK",
            "rows": len(df),
            "buy_count": strong,
            "alert_count": alerts,
            "items": df.to_dict("records"),
            "summary": f"扫描{len(df)}只股票，BUY={strong}，风险提示={alerts}",
        }
