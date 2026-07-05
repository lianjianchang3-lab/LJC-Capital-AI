import pandas as pd

class Build006Commander:
    def __init__(self):
        from core.multisource import MultiSourceRealtimeHub
        self.hub = MultiSourceRealtimeHub()

    def quotes(self):
        return self.hub.score()

    def ljc_score(self):
        df = self.quotes()
        if df.empty:
            return df
        df = df.copy()
        for c in ["change_pct","amount","volume","turnover","risk","LJC实时分"]:
            df[c] = pd.to_numeric(df.get(c,0), errors="coerce").fillna(0)

        df["资金分"] = (df["amount"].rank(pct=True) * 100).round(1)
        df["趋势分"] = (50 + df["change_pct"].clip(-10,10) * 5).clip(0,100).round(1)
        df["量能分"] = (df["volume"].rank(pct=True) * 100).round(1)
        df["风险分"] = (100 - df["risk"]).clip(0,100).round(1)

        df["LJC评分"] = (
            df["资金分"]*0.30 +
            df["趋势分"]*0.25 +
            df["量能分"]*0.15 +
            df["风险分"]*0.15 +
            df["LJC实时分"]*0.15
        ).round(1)

        df["星级"] = "★★★"
        df.loc[df["LJC评分"]>=75, "星级"] = "★★★★"
        df.loc[df["LJC评分"]>=88, "星级"] = "★★★★★"

        df["主升浪阶段"] = "观察"
        df.loc[(df["趋势分"]>=70)&(df["资金分"]>=70), "主升浪阶段"] = "启动/建仓"
        df.loc[(df["趋势分"]>=80)&(df["资金分"]>=80)&(df["量能分"]>=70), "主升浪阶段"] = "主升浪"
        df.loc[(df["change_pct"]>=7)&(df["量能分"]>=85), "主升浪阶段"] = "加速浪"
        df.loc[(df["risk"]>=75)|(df["change_pct"]<=-5), "主升浪阶段"] = "风险/派发"

        df["操作建议"] = "观察"
        df.loc[(df["LJC评分"]>=88)&(df["risk"]<=60), "操作建议"] = "买入关注"
        df.loc[(df["LJC评分"]>=75)&(df["risk"]<=70), "操作建议"] = "小仓观察"
        df.loc[(df["risk"]>=75)|(df["change_pct"]<=-5), "操作建议"] = "减仓/回避"

        df["建议仓位"] = "0%-3%"
        df.loc[df["操作建议"]=="小仓观察", "建议仓位"] = "3%-8%"
        df.loc[df["操作建议"]=="买入关注", "建议仓位"] = "8%-15%"
        df.loc[df["操作建议"]=="减仓/回避", "建议仓位"] = "0%"

        df["止损参考"] = (df["price"]*0.93).round(2)
        df["目标一"] = (df["price"]*1.10).round(2)
        df["目标二"] = (df["price"]*1.20).round(2)

        return df.sort_values("LJC评分", ascending=False)

    def dashboard(self):
        df = self.ljc_score()
        if df.empty:
            return {"status":"NO DATA","market_score":0,"position":"0%","risk":"未知","summary":"暂无数据","top":[]}
        market_score = round(float(df["LJC评分"].mean()),1)
        risk_avg = round(float(pd.to_numeric(df.get("risk",0), errors="coerce").fillna(0).mean()),1)
        if market_score >= 80 and risk_avg <= 60:
            position = "70%-85%"
            risk = "低-中"
        elif market_score >= 65:
            position = "45%-65%"
            risk = "中"
        else:
            position = "20%-40%"
            risk = "偏高"
        top = df.head(10).to_dict("records")
        return {
            "status":"OK",
            "market_score":market_score,
            "position":position,
            "risk":risk,
            "buy_count":int((df["操作建议"]=="买入关注").sum()),
            "watch_count":int((df["操作建议"]=="小仓观察").sum()),
            "risk_count":int((df["操作建议"]=="减仓/回避").sum()),
            "summary":f"市场评分 {market_score}，建议仓位 {position}，风险 {risk}",
            "top":top,
        }

    def trading_plan(self):
        df = self.ljc_score()
        if df.empty:
            return {"status":"NO DATA","plans":[]}
        cols = ["code","name","price","change_pct","LJC评分","星级","主升浪阶段","操作建议","建议仓位","止损参考","目标一","目标二"]
        cols = [c for c in cols if c in df.columns]
        return {"status":"OK","plans":df[cols].head(20).to_dict("records")}
