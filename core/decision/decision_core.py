import pandas as pd
from core.data import MarketDataService
from core.factors import ScoreEngine

class DecisionCore:
    def __init__(self, market_service=None, score_engine=None):
        self.market_service = market_service or MarketDataService()
        self.score_engine = score_engine or ScoreEngine()

    def market(self):
        snap = self.market_service.snapshot()
        df = self.stocks()
        if df.empty:
            return {"status":"NO DATA","summary":"暂无数据","health":snap.health()}
        avg = round(float(df["LCRI Score"].mean()), 1)
        risk_score = round(float(df["risk_score"].mean()), 1) if "risk_score" in df.columns else 0
        buy_count = int((df["LCRI Score"] >= 82).sum())
        avoid_count = int((df["LCRI Score"] < 50).sum())
        if avg >= 82:
            state, position = "进攻", "65%-80%"
        elif avg >= 68:
            state, position = "震荡偏强", "45%-65%"
        else:
            state, position = "防守", "20%-40%"
        return {
            "status":"OK",
            "state":state,
            "position":position,
            "lcri_avg":avg,
            "risk_score":risk_score,
            "buy_count":buy_count,
            "avoid_count":avoid_count,
            "summary":f"市场状态：{state}，LCRI均分 {avg}，建议仓位 {position}",
            "health":snap.health(),
        }

    def stocks(self):
        df = self.market_service.dataframe()
        return self.score_engine.score(df)

    def stock(self, code):
        df = self.stocks()
        if df.empty:
            return {"status":"NO DATA","code":code}
        code = str(code).zfill(6)
        row = df[df["code"].astype(str).str.zfill(6) == code]
        if row.empty:
            return {"status":"NOT FOUND","code":code}
        r = row.iloc[0].to_dict()
        r["status"] = "OK"
        r["decision"] = self._decision_from_score(r)
        return r

    def trade_plan(self):
        df = self.stocks()
        if df.empty:
            return pd.DataFrame()
        out = df.copy()
        for c in ["price","LCRI Score","risk_score"]:
            out[c] = pd.to_numeric(out.get(c,0), errors="coerce").fillna(0)
        out["Action"] = "观察"
        out.loc[out["LCRI Score"]>=88, "Action"] = "A类关注"
        out.loc[(out["LCRI Score"]>=75)&(out["LCRI Score"]<88), "Action"] = "B类等待回踩"
        out.loc[out["LCRI Score"]<50, "Action"] = "C类回避"
        out["Buy Zone"] = out.apply(lambda r: f"{round(r['price']*0.98,2)}-{round(r['price']*1.01,2)}" if r["price"]>0 else "-", axis=1)
        out["Stop Loss"] = (out["price"]*0.93).round(2)
        out["Target 1"] = (out["price"]*1.10).round(2)
        out["Target 2"] = (out["price"]*1.20).round(2)
        out["Position"] = "0%-3%"
        out.loc[out["Action"]=="B类等待回踩", "Position"] = "3%-8%"
        out.loc[out["Action"]=="A类关注", "Position"] = "8%-15%"
        out["Reason"] = out["LCRI Evidence"]
        return out.sort_values("LCRI Score", ascending=False)

    def portfolio(self):
        try:
            import pandas as pd
            h = pd.read_csv("data/portfolio/holdings.csv", dtype={"code":str})
        except Exception:
            h = pd.DataFrame()
        plan = self.trade_plan()
        if h.empty or plan.empty:
            return {"status":"NO DATA","summary":"暂无持仓或行情","holdings":[]}
        h["code"] = h["code"].astype(str).str.zfill(6)
        plan["code"] = plan["code"].astype(str).str.zfill(6)
        merged = h.merge(plan, on="code", how="left", suffixes=("_holding",""))
        for c in ["cost","shares","price"]:
            merged[c] = pd.to_numeric(merged.get(c,0), errors="coerce").fillna(0)
        merged["Market Value"] = (merged["price"] * merged["shares"]).round(2)
        merged["PnL"] = (merged["price"] - merged["cost"]) * merged["shares"]
        merged["PnL %"] = merged.apply(lambda r: round((r["price"]-r["cost"])/r["cost"]*100,2) if r["cost"]>0 else 0, axis=1)
        avg_score = round(float(pd.to_numeric(merged.get("LCRI Score",0), errors="coerce").fillna(0).mean()),1)
        return {"status":"OK","summary":f"持仓{len(merged)}只，平均LCRI {avg_score}","holdings":merged.to_dict("records")}

    def morning_report(self):
        m = self.market()
        plan = self.trade_plan()
        lines = ["LJC V5 Morning Report", "="*28, m.get("summary","暂无数据"), ""]
        if not plan.empty:
            lines.append("今日重点：")
            for i, (_, r) in enumerate(plan.head(8).iterrows(), 1):
                lines.append(f"{i}. {r.get('code')} {r.get('name')}｜{r.get('Action')}｜LCRI {r.get('LCRI Score')}｜仓位 {r.get('Position')}")
        return "\n".join(lines)

    def _decision_from_score(self, r):
        score = float(r.get("LCRI Score",0))
        if score >= 88:
            return "A类关注"
        if score >= 75:
            return "B类等待回踩"
        if score < 50:
            return "C类回避"
        return "观察"
