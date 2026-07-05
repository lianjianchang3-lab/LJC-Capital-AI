import pandas as pd


class MarketRadar:
    """
    真实 Market Radar：
    直接复用现有 DecisionCore、AITrader、InstitutionEngine。
    """

    def __init__(self):
        self._decision = None
        self._trader = None
        self._institution = None

    @property
    def decision(self):
        if self._decision is None:
            from core.decision import DecisionCore
            self._decision = DecisionCore()
        return self._decision

    @property
    def trader(self):
        if self._trader is None:
            try:
                from core.trader import AITrader
                self._trader = AITrader()
            except Exception:
                self._trader = False
        return None if self._trader is False else self._trader

    @property
    def institution(self):
        if self._institution is None:
            try:
                from core.institution import InstitutionEngine
                self._institution = InstitutionEngine()
            except Exception:
                self._institution = False
        return None if self._institution is False else self._institution

    def _safe_df(self, df):
        if df is None:
            return pd.DataFrame()
        if isinstance(df, pd.DataFrame):
            return df
        try:
            return pd.DataFrame(df)
        except Exception:
            return pd.DataFrame()

    def lcri_top(self, limit=20):
        try:
            df = self._safe_df(self.decision.trade_plan())
        except Exception:
            df = pd.DataFrame()
        if df.empty:
            return df
        if "LCRI Score" in df.columns:
            return df.sort_values("LCRI Score", ascending=False).head(limit)
        return df.head(limit)

    def trader_top(self, limit=20):
        if self.trader is None:
            return pd.DataFrame()
        try:
            df = self._safe_df(self.trader.signals())
        except Exception:
            df = pd.DataFrame()
        if df.empty:
            return df
        score_col = "AI交易强度" if "AI交易强度" in df.columns else "LCRI Score"
        if score_col in df.columns:
            return df.sort_values(score_col, ascending=False).head(limit)
        return df.head(limit)

    def institution_top(self, limit=20):
        if self.institution is None:
            return pd.DataFrame()
        try:
            df = self._safe_df(self.institution.run())
        except Exception:
            df = pd.DataFrame()
        if df.empty:
            return df
        score_col = "机构共振指数" if "机构共振指数" in df.columns else "LCRI Score"
        if score_col in df.columns:
            return df.sort_values(score_col, ascending=False).head(limit)
        return df.head(limit)

    def risk_top(self, limit=20):
        try:
            df = self._safe_df(self.decision.trade_plan())
        except Exception:
            return pd.DataFrame()
        if df.empty:
            return df
        out = df.copy()
        for c in ["risk_score", "LCRI Score", "change_pct"]:
            if c not in out.columns:
                out[c] = 0
            out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0)
        out["风险热度"] = ((100 - out["risk_score"]) * 0.7 + out["change_pct"].apply(lambda x: 20 if x < -3 else 0)).round(1)
        return out.sort_values("风险热度", ascending=False).head(limit)

    def health(self):
        try:
            market = self.decision.market()
        except Exception as e:
            market = {"status": "ERROR", "summary": str(e)}

        lcri = self.lcri_top(200)
        trader = self.trader_top(200)
        inst = self.institution_top(200)

        lcri_count = len(lcri)
        trader_count = len(trader)
        inst_count = len(inst)

        avg = market.get("lcri_avg", 0) if isinstance(market, dict) else 0
        state = market.get("state", "未知") if isinstance(market, dict) else "未知"
        position = market.get("position", "-") if isinstance(market, dict) else "-"

        return {
            "status": "OK" if lcri_count > 0 else "NO DATA",
            "market_state": state,
            "suggested_position": position,
            "lcri_avg": avg,
            "lcri_count": lcri_count,
            "trader_count": trader_count,
            "institution_count": inst_count,
            "summary": f"市场{state}，LCRI均分{avg}，建议仓位{position}，扫描{lcri_count}条。",
        }

    def snapshot(self):
        return {
            "health": self.health(),
            "lcri_top": self.lcri_top(20).to_dict("records"),
            "trader_top": self.trader_top(20).to_dict("records"),
            "institution_top": self.institution_top(20).to_dict("records"),
            "risk_top": self.risk_top(20).to_dict("records"),
        }
