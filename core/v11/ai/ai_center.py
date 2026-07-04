import pandas as pd
from core.v11.data.data_center import DataCenterV11

class AICenterV11:
    def decisions(self):
        df = DataCenterV11().quotes()
        if df.empty:
            return {"status":"NO DATA","summary":"等待数据","items":[]}
        df = df.copy()
        for col in ["change_pct","amount","turnover","main_inflow","trend","capital","risk","lia","quality"]:
            df[col] = pd.to_numeric(df.get(col,0), errors="coerce").fillna(0)
        df["LCRI"] = (df["amount"].rank(pct=True)*20 + df["turnover"].rank(pct=True)*12 + df["main_inflow"]*25 + df["change_pct"].clip(-10,10)*2 + df["capital"]*0.2 + df["lia"]*0.2 - df["risk"]*0.2).round(1)
        df["AI综合分"] = (df["LCRI"]*0.35 + df["trend"]*0.20 + df["capital"]*0.15 + df["lia"]*0.15 + (100-df["risk"])*0.15).round(1)
        df["AI决策"] = "观察"
        df.loc[(df["AI综合分"]>=85)&(df["risk"]<=60), "AI决策"] = "重点买入关注"
        df.loc[(df["AI综合分"]>=75)&(df["risk"]<=70), "AI决策"] = "买入观察"
        df.loc[(df["risk"]>=75)|(df["change_pct"]<=-5), "AI决策"] = "风险回避"
        df["建议仓位"] = "0%-3%"
        df.loc[df["AI决策"]=="买入观察","建议仓位"]="5%-10%"
        df.loc[df["AI决策"]=="重点买入关注","建议仓位"]="10%-18%"
        df.loc[df["AI决策"]=="风险回避","建议仓位"]="0%"
        df["理由"] = df.apply(lambda r: f"LCRI={r['LCRI']} 趋势={r['trend']} LIA={r['lia']} 风险={r['risk']}", axis=1)
        return {"status":"OK","summary":f"AI决策完成：{len(df)}只。","items":df.sort_values("AI综合分", ascending=False).to_dict("records")}
