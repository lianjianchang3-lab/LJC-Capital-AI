from core.strategy_v3 import ScoreV3

class CapitalIntelligence:
    def analyze(self):
        df = ScoreV3().table()
        if df.empty:
            return {"status": "NO DATA", "capital_regime": "UNKNOWN", "leaders": []}
        avg_capital = round(float(df["capital"].mean()), 1) if "capital" in df.columns else 0
        if avg_capital >= 75:
            regime = "资金强势"
        elif avg_capital >= 60:
            regime = "资金中性"
        else:
            regime = "资金偏弱"
        leaders = df.sort_values("capital", ascending=False).head(10).to_dict("records") if "capital" in df.columns else []
        return {
            "status": "OK",
            "capital_regime": regime,
            "avg_capital": avg_capital,
            "leaders": leaders,
            "note": "资金中心当前基于capital.csv与评分模型。",
        }
