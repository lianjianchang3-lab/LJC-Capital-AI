import pandas as pd
from core.v11.data.data_center import DataCenterV11

class RiskCenterV11:
    def assess(self):
        df = DataCenterV11().quotes()
        if df.empty:
            return {"status":"NO DATA","summary":"等待数据","items":[],"portfolio_risk":"未知"}
        df = df.copy()
        for col in ["risk","change_pct","turnover","amount"]:
            df[col] = pd.to_numeric(df.get(col,0), errors="coerce").fillna(0)
        df["风险等级"]="中"
        df.loc[(df["risk"]<=45)&(df["change_pct"]>-3),"风险等级"]="低"
        df.loc[(df["risk"]>=75)|(df["change_pct"]<=-5),"风险等级"]="高"
        high = int((df["风险等级"]=="高").sum())
        avg = round(float(df["risk"].mean()),1)
        pr = "高" if avg>=70 else "中" if avg>=50 else "低"
        return {"status":"OK","summary":f"组合风险={pr}，高风险{high}只。","items":df.sort_values("risk", ascending=False).to_dict("records"),"portfolio_risk":pr,"avg_risk":avg}
