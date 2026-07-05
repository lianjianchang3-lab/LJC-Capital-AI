import pandas as pd
from core.pro_v20.alpha.alpha_engine_v2 import AlphaEngineV2
from core.pro_v20.capital.capital_engine_v2 import CapitalEngineV2
from core.pro_v20.risk.risk_engine_v2 import RiskEngineV2

class TradePlannerV2:
    def __init__(self):
        self.alpha = AlphaEngineV2()
        self.capital = CapitalEngineV2()
        self.risk = RiskEngineV2()

    def plan(self):
        a = self.alpha.run()
        c = self.capital.run()
        r = self.risk.run()
        if a.empty:
            return pd.DataFrame()

        cols_c = ["code","资金共振","资金状态","主力模拟分"]
        cols_r = ["code","综合风险","风险等级","止损位","第一目标","第二目标"]
        df = a.merge(c[cols_c], on="code", how="left").merge(r[cols_r], on="code", how="left")

        df["建议仓位"] = "0%-3%"
        df.loc[df["最终动作"]=="小仓试探", "建议仓位"] = "3%-8%"
        df.loc[df["最终动作"]=="买入关注", "建议仓位"] = "8%-15%"
        df.loc[df["风险等级"]=="高", "建议仓位"] = "0%"

        df["买入区间"] = df.apply(lambda x: f"{round(x['price']*0.98,2)}-{round(x['price']*1.01,2)}" if x.get("price",0)>0 else "-", axis=1)
        df["交易理由"] = df.apply(lambda x: f"Alpha {x.get('Alpha2.0')}｜资金共振 {x.get('资金共振')}｜风险 {x.get('风险等级')}｜胜率 {x.get('胜率估计')}%", axis=1)

        return df.sort_values(["Alpha2.0","资金共振"], ascending=False)

    def commander_summary(self):
        df = self.plan()
        if df.empty:
            return {"status":"NO DATA","summary":"暂无数据"}
        avg = round(float(df["Alpha2.0"].mean()),1)
        risk = round(float(df["综合风险"].mean()),1)
        buy = int((df["最终动作"]=="买入关注").sum())
        if avg >= 80 and risk < 50:
            mode, pos = "积极进攻", "65%-80%"
        elif avg >= 65 and risk < 65:
            mode, pos = "谨慎进攻", "45%-65%"
        else:
            mode, pos = "防守等待", "20%-40%"
        return {
            "status":"OK",
            "alpha":avg,
            "risk":risk,
            "mode":mode,
            "position":pos,
            "buy_count":buy,
            "summary":f"Alpha {avg}，风险 {risk}，模式：{mode}，建议仓位 {pos}",
            "top":df.head(10).to_dict("records"),
        }
