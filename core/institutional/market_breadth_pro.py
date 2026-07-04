from core.strategy_v3 import ScoreV3

class MarketBreadthPro:
    def snapshot(self):
        df = ScoreV3().table()
        if df.empty:
            return {"status": "NO DATA"}
        strong = int((df["investment_score"] >= 75).sum())
        leaders = int((df["investment_score"] >= 85).sum())
        weak = int((df["investment_score"] < 60).sum())
        total = len(df)
        breadth = round(strong / total * 100, 1) if total else 0
        if breadth >= 60:
            emotion = "启动/升温"
        elif breadth >= 35:
            emotion = "结构性"
        else:
            emotion = "防御/冰点"
        return {
            "status": "OK",
            "breadth_pct": breadth,
            "strong_count": strong,
            "leader_count": leaders,
            "weak_count": weak,
            "emotion_cycle": emotion,
            "leader_table": df.head(5).to_dict("records"),
        }
