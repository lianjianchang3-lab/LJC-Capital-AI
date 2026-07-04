from core.strategy_v3 import ScoreV3
from core.institutional import MarketBreadthPro
from core.capital_intel import CapitalIntelligence

class AIScoreV4:
    """
    Build301-340: AI Score V4
    多因子评分：Trend / Capital / LIA / Risk / Quality / Market Breadth / Capital Regime
    """
    def table(self):
        df = ScoreV3().table()
        if df.empty:
            return df

        df = df.copy()
        breadth = MarketBreadthPro().snapshot()
        capital_regime = CapitalIntelligence().analyze()

        breadth_bonus = 5 if breadth.get("breadth_pct", 0) >= 50 else -3
        capital_bonus = 4 if capital_regime.get("capital_regime") == "资金强势" else 0

        df["market_breadth_factor"] = breadth.get("breadth_pct", 0)
        df["capital_regime_factor"] = capital_regime.get("capital_regime")

        df["ai_score_v4"] = (
            df["trend"] * 0.22 +
            df["capital"] * 0.30 +
            df["lia"] * 0.23 +
            (100 - df["risk"]) * 0.15 +
            df["quality"] * 0.10 +
            breadth_bonus +
            capital_bonus
        ).clip(0, 100).round(1)

        def label(row):
            s = row["ai_score_v4"]
            r = row["risk"]
            if s >= 85 and r <= 65:
                return "BUY"
            if s >= 75 and r <= 70:
                return "WATCH_BUY"
            if s >= 65:
                return "HOLD/WATCH"
            if r >= 75:
                return "REDUCE"
            return "AVOID"

        df["ai_decision_v4"] = df.apply(label, axis=1)
        df["explain_v4"] = df.apply(
            lambda r: f"趋势{r['trend']} 资金{r['capital']} LIA{r['lia']} 风险{r['risk']} 市场宽度{r['market_breadth_factor']}",
            axis=1,
        )
        return df.sort_values("ai_score_v4", ascending=False)
