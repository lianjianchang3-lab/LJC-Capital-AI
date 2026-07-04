import pandas as pd
from core.v93.realtime import RealtimeCore

class V93MarketScanner:
    """
    V9.3 Sprint B：实时市场扫描。
    基于 Sprint A RealtimeCore，优先 AKShare，失败 CSV fallback。
    """
    def __init__(self):
        self.core = RealtimeCore()

    def scan(self, top_n=50):
        df = self.core.quotes(prefer_live=True)
        if df is None or df.empty:
            return {"status": "NO_DATA", "summary": "暂无行情数据", "items": []}

        df = df.copy()
        for col in ["price","change_pct","amount","volume","turnover","main_inflow","trend","capital","risk","quality","lia"]:
            if col not in df.columns:
                df[col] = 0
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # AKShare 全市场数据通常没有 capital/lia 等内部字段，这里用行情字段生成临时因子
        df["amount_rank_score"] = df["amount"].rank(pct=True).fillna(0) * 100
        df["turnover_rank_score"] = df["turnover"].rank(pct=True).fillna(0) * 100
        df["momentum_score"] = (df["change_pct"].clip(-10, 10) + 10) * 5

        # 若内部字段为空，用行情因子补足
        df["capital_x"] = df["capital"]
        df.loc[df["capital_x"] == 0, "capital_x"] = df["amount_rank_score"]
        df["trend_x"] = df["trend"]
        df.loc[df["trend_x"] == 0, "trend_x"] = df["momentum_score"]
        df["lia_x"] = df["lia"]
        df.loc[df["lia_x"] == 0, "lia_x"] = (df["amount_rank_score"] * 0.6 + df["turnover_rank_score"] * 0.4)
        df["risk_x"] = df["risk"]
        df.loc[df["risk_x"] == 0, "risk_x"] = (100 - df["momentum_score"]).clip(20, 80)

        df["ai_score_v3"] = (
            df["capital_x"] * 0.32
            + df["trend_x"] * 0.28
            + df["lia_x"] * 0.22
            + df["quality"] * 0.08
            - df["risk_x"] * 0.10
            + df["change_pct"].clip(-10, 10) * 1.5
        ).round(1)

        df["decision"] = "WATCH"
        df.loc[(df["ai_score_v3"] >= 85) & (df["risk_x"] <= 55), "decision"] = "BUY"
        df.loc[(df["ai_score_v3"] >= 75) & (df["ai_score_v3"] < 85), "decision"] = "WATCH_BUY"
        df.loc[(df["change_pct"] <= -4) | (df["risk_x"] >= 75), "decision"] = "RISK_ALERT"
        df.loc[df["ai_score_v3"] < 45, "decision"] = "AVOID"

        df["position"] = "0%"
        df.loc[df["decision"] == "WATCH", "position"] = "0%-3%"
        df.loc[df["decision"] == "WATCH_BUY", "position"] = "3%-8%"
        df.loc[df["decision"] == "BUY", "position"] = "8%-12%"

        df["reason"] = (
            "AI=" + df["ai_score_v3"].astype(str)
            + " 资金=" + df["capital_x"].round(1).astype(str)
            + " 趋势=" + df["trend_x"].round(1).astype(str)
            + " 风险=" + df["risk_x"].round(1).astype(str)
        )

        df = df.sort_values("ai_score_v3", ascending=False)
        top = df.head(top_n)
        return {
            "status": "OK",
            "source": str(df["source"].iloc[0]) if "source" in df.columns and len(df) else "unknown",
            "rows": len(df),
            "buy_count": int((df["decision"] == "BUY").sum()),
            "watch_buy_count": int((df["decision"] == "WATCH_BUY").sum()),
            "risk_count": int((df["decision"] == "RISK_ALERT").sum()),
            "summary": f"扫描{len(df)}只，BUY={(df['decision']=='BUY').sum()}，WATCH_BUY={(df['decision']=='WATCH_BUY').sum()}，RISK={(df['decision']=='RISK_ALERT').sum()}",
            "items": top.to_dict("records"),
        }
