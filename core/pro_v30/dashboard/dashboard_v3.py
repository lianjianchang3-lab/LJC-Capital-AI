import pandas as pd
from core.pro_v30.watchlist.watchlist_manager import WatchlistManager
from core.pro_v30.portfolio.holding_manager import HoldingManager

class DashboardV3:
    def __init__(self):
        self.watch = WatchlistManager()
        self.hold = HoldingManager()

    def _planner(self):
        try:
            from core.pro_v20.tradeplan.trade_planner_v2 import TradePlannerV2
            return TradePlannerV2().plan()
        except Exception:
            return pd.DataFrame()

    def watchlist_decision(self):
        w = self.watch.load()
        p = self._planner()
        if w.empty:
            return w
        if p is None or p.empty or "code" not in p.columns:
            return w
        p = p.copy()
        p["code"] = p["code"].astype(str).str.zfill(6)
        out = w.merge(p, on="code", how="left", suffixes=("_watch",""))
        if "name" not in out.columns and "name_watch" in out.columns:
            out["name"] = out["name_watch"]
        return out.sort_values(["star","sort"], ascending=[False, True])

    def portfolio_decision(self):
        h = self.hold.load()
        p = self._planner()
        if h.empty:
            return h
        if p is None or p.empty or "code" not in p.columns:
            return h
        p = p.copy()
        p["code"] = p["code"].astype(str).str.zfill(6)
        out = h.merge(p, on="code", how="left", suffixes=("_holding",""))
        for c in ["cost","shares","price","Alpha2.0","综合风险"]:
            if c not in out.columns:
                out[c] = 0
            out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0)
        out["市值"] = (out["price"] * out["shares"]).round(2)
        out["成本金额"] = (out["cost"] * out["shares"]).round(2)
        out["浮盈亏"] = (out["市值"] - out["成本金额"]).round(2)
        out["浮盈亏%"] = out.apply(lambda r: round((r["price"]-r["cost"])/r["cost"]*100,2) if r["cost"] else 0, axis=1)
        out["持仓动作"] = "观察"
        out.loc[(out["Alpha2.0"]>=82)&(out["综合风险"]<60), "持仓动作"] = "继续持有/可加仓"
        out.loc[(out["综合风险"]>=70)|(out["浮盈亏%"]<=-8), "持仓动作"] = "减仓/止损检查"
        return out

    def summary(self):
        p = self._planner()
        if p is None or p.empty:
            return {"status":"NO DATA","summary":"暂无交易计划","top":[]}
        avg = round(float(pd.to_numeric(p.get("Alpha2.0",0), errors="coerce").fillna(0).mean()),1)
        risk = round(float(pd.to_numeric(p.get("综合风险",0), errors="coerce").fillna(0).mean()),1)
        if avg >= 80 and risk < 50:
            mode, pos = "积极进攻", "65%-80%"
        elif avg >= 65:
            mode, pos = "谨慎进攻", "45%-65%"
        else:
            mode, pos = "防守等待", "20%-40%"
        return {"status":"OK","alpha":avg,"risk":risk,"mode":mode,"position":pos,"summary":f"Alpha {avg}｜风险 {risk}｜{mode}｜仓位 {pos}","top":p.head(8).to_dict("records")}
