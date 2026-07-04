import pandas as pd
from core.provider import ProviderManager

class InstitutionIntelligenceCore:
    def __init__(self, provider=None):
        self.provider = provider or ProviderManager()

    def _col(self, df, names):
        for n in names:
            if n in df.columns:
                return n
        return None

    def score(self):
        q = self.provider.get_quotes()
        c = self.provider.get_capital()
        if q.empty:
            return pd.DataFrame(columns=["code","name","trend","capital","risk","quality","lia","rank"])

        price_col = self._col(q, ["price","最新价","现价","close","实时价"])
        chg_col = self._col(q, ["change_pct","涨跌幅","涨幅"])
        name_col = self._col(q, ["name","名称","证券名称"])

        main_col = None
        if not c.empty and "code" in c.columns:
            main_col = self._col(c, ["net_main","主力净流入","主力净额","main_inflow"])
            merged = q.merge(c[["code", main_col]] if main_col else c[["code"]], on="code", how="left")
        else:
            merged = q.copy()

        rows = []
        for _, r in merged.iterrows():
            change = float(pd.to_numeric(pd.Series([r.get(chg_col, 0)]), errors="coerce").fillna(0).iloc[0]) if chg_col else 0
            main = float(pd.to_numeric(pd.Series([r.get(main_col, 0)]), errors="coerce").fillna(0).iloc[0]) if main_col else 0
            trend = max(0, min(100, 65 + change * 4))
            capital = max(0, min(100, 60 + main * 12))
            risk = max(0, min(100, 50 + (20 if change < -3 else 0) + (15 if change > 6 else 0) - (8 if main > 0 else 0)))
            quality = max(0, min(100, 70 + (5 if main > 0 and change > 0 else 0)))
            lia = round(trend*0.30 + capital*0.35 + quality*0.15 + (100-risk)*0.20, 1)
            if lia >= 88: rank = "A+"
            elif lia >= 80: rank = "A"
            elif lia >= 70: rank = "B"
            elif lia >= 60: rank = "C"
            else: rank = "D"
            rows.append({
                "code": r.get("code",""),
                "name": r.get(name_col, r.get("code","")) if name_col else r.get("code",""),
                "price": float(pd.to_numeric(pd.Series([r.get(price_col, 0)]), errors="coerce").fillna(0).iloc[0]) if price_col else 0,
                "change_pct": change,
                "main_inflow": main,
                "trend": round(trend,1),
                "capital": round(capital,1),
                "risk": round(risk,1),
                "quality": round(quality,1),
                "lia": lia,
                "rank": rank,
            })
        return pd.DataFrame(rows).sort_values("lia", ascending=False)
