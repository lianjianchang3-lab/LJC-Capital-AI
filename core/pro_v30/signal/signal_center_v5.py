import pandas as pd

class SignalCenterV5:
    def __init__(self):
        from core.pro_v20.tradeplan.trade_planner_v2 import TradePlannerV2
        self.planner = TradePlannerV2()

    def signals(self):
        df = self.planner.plan()
        if df is None or df.empty:
            return pd.DataFrame()

        df = df.copy()
        for c in ["price","Alpha2.0","资金共振","综合风险","胜率估计","change_pct"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        df["第一买点"] = (df["price"] * 0.985).round(2)
        df["第二买点"] = (df["price"] * 0.965).round(2)
        df["突破买点"] = (df["price"] * 1.025).round(2)
        df["减仓位"] = (df["price"] * 1.12).round(2)
        df["清仓警戒"] = (df["price"] * 0.91).round(2)
        df["止损"] = (df["price"] * 0.93).round(2)
        df["目标一"] = (df["price"] * 1.10).round(2)
        df["目标二"] = (df["price"] * 1.20).round(2)

        df["信号"] = "观察"
        df.loc[(df["Alpha2.0"]>=85)&(df["资金共振"]>=70)&(df["综合风险"]<55), "信号"] = "买入"
        df.loc[(df["Alpha2.0"]>=75)&(df["综合风险"]<65), "信号"] = "小仓试探"
        df.loc[(df["综合风险"]>=70)|(df["change_pct"]<=-5), "信号"] = "减仓/回避"

        df["信号强度"] = (
            df["Alpha2.0"]*0.45 + df["资金共振"]*0.35 + (100-df["综合风险"])*0.20
        ).round(1)

        df["一句话建议"] = df.apply(
            lambda r: f"{r.get('name')}：{r.get('信号')}，建议仓位{r.get('建议仓位','0%-3%')}，止损{r.get('止损')}，目标{r.get('目标一')}/{r.get('目标二')}",
            axis=1
        )
        return df.sort_values("信号强度", ascending=False)
