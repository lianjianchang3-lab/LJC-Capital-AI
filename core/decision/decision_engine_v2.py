import pandas as pd
from core.provider import ProviderManager

class DecisionEngineV2:
    def __init__(self, provider=None):
        self.provider = provider or ProviderManager()

    def _col(self, df, names):
        for n in names:
            if n in df.columns:
                return n
        return None

    def decisions(self):
        q = self.provider.get_quotes()
        c = self.provider.get_capital()
        if q.empty:
            return pd.DataFrame(columns=["code", "name", "price", "lia", "risk", "decision", "reason"])

        price_col = self._col(q, ["price", "最新价", "现价", "close", "实时价"])
        change_col = self._col(q, ["change_pct", "涨跌幅", "涨幅"])
        name_col = self._col(q, ["name", "名称", "证券名称"])

        main_col = None
        if not c.empty and "code" in c.columns:
            main_col = self._col(c, ["net_main", "主力净流入", "主力净额", "main_inflow"])
            merged = q.merge(c[["code", main_col]] if main_col else c[["code"]], on="code", how="left")
        else:
            merged = q.copy()

        rows = []
        for _, r in merged.iterrows():
            price = float(pd.to_numeric(pd.Series([r.get(price_col, 0)]), errors="coerce").fillna(0).iloc[0]) if price_col else 0
            change = float(pd.to_numeric(pd.Series([r.get(change_col, 0)]), errors="coerce").fillna(0).iloc[0]) if change_col else 0
            main = float(pd.to_numeric(pd.Series([r.get(main_col, 0)]), errors="coerce").fillna(0).iloc[0]) if main_col else 0
            capital_score = max(0, min(100, 60 + main * 10))
            trend_score = max(0, min(100, 65 + change * 3))
            risk = max(0, min(100, 50 + (15 if change < -3 else 0) + (20 if change > 6 else 0)))
            lia = round(capital_score * 0.45 + trend_score * 0.35 + (100 - risk) * 0.20, 1)
            if lia >= 85:
                decision, action = "Diamond", "持有/低吸"
            elif lia >= 75:
                decision, action = "Opportunity", "等待确认"
            elif lia >= 65:
                decision, action = "Watch", "观察"
            else:
                decision, action = "Avoid", "暂不参与"
            rows.append({"code": r.get("code", ""), "name": r.get(name_col, r.get("code", "")) if name_col else r.get("code", ""), "price": price, "change_pct": change, "main_inflow": main, "lia": lia, "risk": risk, "decision": decision, "action": action, "reason": f"趋势{trend_score:.0f}/资金{capital_score:.0f}/风险{risk:.0f}"})
        return pd.DataFrame(rows).sort_values("lia", ascending=False)
