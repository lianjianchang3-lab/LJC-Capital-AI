import pandas as pd
from core.v92.live import V92LiveDataEngine

class V92LiveMonitor:
    def scan(self):
        df = V92LiveDataEngine().get_quotes(prefer_live=True)
        if df.empty:
            return {"status": "NO DATA", "summary": "等待行情", "items": []}

        df = df.copy()
        for col in ["change_pct","main_inflow","trend","capital","lia","risk","amount","turnover"]:
            if col not in df.columns:
                df[col] = 0
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        df["live_score"] = (
            df["change_pct"].clip(-10,10) * 2
            + df["capital"] * 0.25
            + df["lia"] * 0.25
            + df["trend"] * 0.20
            + df["main_inflow"] * 10
            - df["risk"] * 0.20
        ).round(1)

        df["live_signal"] = "WATCH"
        df.loc[(df["live_score"] >= 80) & (df["risk"] <= 60), "live_signal"] = "BUY"
        df.loc[(df["change_pct"] <= -4) | (df["risk"] >= 75), "live_signal"] = "RISK"

        top = df.sort_values("live_score", ascending=False).head(50)
        return {
            "status": "OK",
            "summary": f"实时扫描 {len(df)} 条，BUY={(df['live_signal']=='BUY').sum()}，RISK={(df['live_signal']=='RISK').sum()}",
            "items": top.to_dict("records"),
        }
