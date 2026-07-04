import pandas as pd
from core.v10.market import V10MarketHub

class V10SectorRotation:
    def rank(self):
        df = V10MarketHub().quotes()
        if df.empty:
            return {"status": "NO DATA", "items": [], "summary": "等待行情数据"}
        df = df.copy()
        if "sector" not in df.columns:
            df["sector"] = "未知"
        for col in ["change_pct","main_inflow","amount","capital","lia","risk"]:
            df[col] = pd.to_numeric(df.get(col, 0), errors="coerce").fillna(0)
        g = df.groupby("sector").agg(
            股票数=("code","count"),
            平均涨幅=("change_pct","mean"),
            资金均值=("main_inflow","mean"),
            成交额=("amount","sum"),
            资本评分=("capital","mean"),
            LIA=("lia","mean"),
            风险=("risk","mean"),
        ).reset_index()
        g["板块强度"] = (
            g["平均涨幅"].clip(-10, 10) * 2
            + g["资金均值"] * 20
            + g["成交额"].rank(pct=True) * 20
            + g["资本评分"] * 0.2
            + g["LIA"] * 0.2
            - g["风险"] * 0.15
        ).round(1)
        g = g.sort_values("板块强度", ascending=False)
        return {
            "status": "OK",
            "summary": f"行业轮动扫描完成：{len(g)}个板块。",
            "items": g.to_dict("records"),
        }
