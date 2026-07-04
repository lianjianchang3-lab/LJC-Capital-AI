import pandas as pd
from core.v105.data.live_hub import LiveHub105
from core.v105.lcri.lcri_engine import LCRIEngine105

class SectorEngine105:
    def rank(self):
        df = LiveHub105().quotes()
        if df.empty:
            return {"status":"NO DATA","summary":"等待行情数据","items":[]}
        lcri = pd.DataFrame(LCRIEngine105().calculate().get("items",[]))
        if not lcri.empty and "code" in lcri.columns:
            df = df.merge(lcri[["code","LCRI"]], on="code", how="left")
        else:
            df["LCRI"] = 0
        if "sector" not in df.columns:
            df["sector"]="未知"
        for col in ["change_pct","amount","turnover","capital","lia","risk","LCRI"]:
            df[col] = pd.to_numeric(df.get(col,0), errors="coerce").fillna(0)
        g = df.groupby("sector").agg(
            股票数=("code","count"),
            平均涨幅=("change_pct","mean"),
            成交额=("amount","sum"),
            平均LCRI=("LCRI","mean"),
            平均LIA=("lia","mean"),
            平均风险=("risk","mean"),
        ).reset_index()
        g["行业热度"] = (g["平均涨幅"].clip(-10,10)*2 + g["成交额"].rank(pct=True)*20 + g["平均LCRI"]*0.35 + g["平均LIA"]*0.2 - g["平均风险"]*0.15).round(1)
        g = g.sort_values("行业热度", ascending=False)
        return {"status":"OK","summary":f"行业轮动完成：{len(g)}个板块。","items":g.to_dict("records")}
