from core.strategy_v3 import ScoreV3

class SelectionCenter:
    def __init__(self):
        self.score = ScoreV3()

    def scan(self):
        df = self.score.table()
        if df.empty:
            return {"status": "NO DATA", "top10": [], "main_wave": [], "leaders": []}
        top = df.head(10).to_dict("records")
        main_wave = df[(df["trend"] >= 75) & (df["capital"] >= 70)].head(10).to_dict("records")
        leaders = df.sort_values(["investment_score","capital"], ascending=False).head(5).to_dict("records")
        return {"status": "OK", "top10": top, "main_wave": main_wave, "leaders": leaders}
