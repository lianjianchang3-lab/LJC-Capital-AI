import pandas as pd
from core.v10.market import V10MarketHub

class V10FundMonitor:
    """
    Level2资金监控基础版。
    如没有真实Level2字段，则用 main_inflow / amount / turnover 估算资金强度。
    """
    def analyze(self):
        df = V10MarketHub().quotes()
        if df.empty:
            return {"status": "NO DATA", "items": [], "summary": "等待行情数据"}
        df = df.copy()
        for col in ["main_inflow","amount","turnover","change_pct","capital","risk"]:
            df[col] = pd.to_numeric(df.get(col, 0), errors="coerce").fillna(0)
        df["主力强度"] = (
            df["main_inflow"] * 35
            + df["amount"].rank(pct=True) * 25
            + df["turnover"].rank(pct=True) * 15
            + df["change_pct"].clip(-10, 10) * 2
            + df["capital"] * 0.2
            - df["risk"] * 0.15
        ).round(1)
        df["资金标签"] = "普通"
        df.loc[df["主力强度"] >= 80, "资金标签"] = "强资金"
        df.loc[df["主力强度"] <= 35, "资金标签"] = "资金弱"
        top = df.sort_values("主力强度", ascending=False)
        return {
            "status": "OK",
            "summary": f"资金监控完成：{len(df)}只，强资金{int((df['资金标签']=='强资金').sum())}只。",
            "items": top.to_dict("records"),
        }
