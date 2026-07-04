import pandas as pd
from core.v105.data.live_hub import LiveHub105

class LCRIEngine105:
    def calculate(self):
        df = LiveHub105().quotes()
        if df.empty:
            return {"status":"NO DATA","summary":"等待行情数据","items":[]}
        df = df.copy()
        for col in ["amount","turnover","change_pct","main_inflow","capital","trend","lia","risk"]:
            df[col] = pd.to_numeric(df.get(col,0), errors="coerce").fillna(0)
        df["LCRI"] = (
            df["amount"].rank(pct=True)*20 +
            df["turnover"].rank(pct=True)*15 +
            df["change_pct"].clip(-10,10)*2 +
            df["main_inflow"]*25 +
            df["capital"]*0.18 +
            df["trend"]*0.16 +
            df["lia"]*0.16 -
            df["risk"]*0.18
        ).round(1)
        df["资金结论"] = "普通"
        df.loc[df["LCRI"]>=85,"资金结论"]="主力强攻"
        df.loc[(df["LCRI"]>=70)&(df["LCRI"]<85),"资金结论"]="资金共振"
        df.loc[df["LCRI"]<=35,"资金结论"]="资金偏弱"
        df = df.sort_values("LCRI", ascending=False)
        return {"status":"OK","summary":f"LCRI完成：{len(df)}只，强信号{int((df['LCRI']>=70).sum())}只。","items":df.to_dict("records")}
