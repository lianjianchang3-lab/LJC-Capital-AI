from core.intelligence import InstitutionIntelligenceCore

class InstitutionTracker:
    def __init__(self, core=None):
        self.core = core or InstitutionIntelligenceCore()

    def track(self):
        df = self.core.score()
        if df.empty:
            return {"status": "NO DATA", "rows": []}
        rows = []
        for _, r in df.iterrows():
            if r["capital"] >= 80 and r["trend"] >= 70:
                label = "连续增仓候选"
            elif r["capital"] < 45:
                label = "资金流出观察"
            else:
                label = "普通跟踪"
            rows.append({
                "code": r["code"],
                "name": r["name"],
                "capital": r["capital"],
                "trend": r["trend"],
                "lia": r["lia"],
                "label": label,
            })
        return {"status": "OK", "rows": rows}
