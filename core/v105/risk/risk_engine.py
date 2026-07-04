import pandas as pd
from core.v105.data.live_hub import LiveHub105

class RiskEngine105:
    def assess(self):
        df = LiveHub105().quotes()
        if df.empty:
            return {"status":"NO DATA","summary":"等待行情数据","items":[]}
        df = df.copy()
        for col in ["change_pct","risk","turnover","amount"]:
            df[col] = pd.to_numeric(df.get(col,0), errors="coerce").fillna(0)
        df["风险等级"] = "中"
        df.loc[(df["risk"]<=45)&(df["change_pct"]>-3),"风险等级"]="低"
        df.loc[(df["risk"]>=70)|(df["change_pct"]<=-5),"风险等级"]="高"
        return {"status":"OK","summary":f"风险评估完成：高风险{int((df['风险等级']=='高').sum())}只。","items":df.to_dict("records")}
