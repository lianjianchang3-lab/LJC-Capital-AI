from core.scoring import StockScoringV2

class SectorRotation:
    def __init__(self, scorer=None):
        self.scorer = scorer or StockScoringV2()

    def analyze(self):
        df = self.scorer.score()
        if df.empty:
            return {"status": "NO DATA", "leaders": []}
        leaders = df.head(5)[["code","name","score2","capital","trend"]].to_dict("records")
        return {
            "status": "OK",
            "theme": "商业航天 / AI基础设施 / 高端制造",
            "leaders": leaders,
            "message": "当前按个股强弱估算板块轮动，V8.2 可接入真实板块数据。",
        }
