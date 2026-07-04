from core.strategy_v3 import ScoreV3

class InstitutionCapitalMatrix:
    def analyze(self):
        df = ScoreV3().table()
        if df.empty:
            return {"status": "NO DATA", "matrix": [], "summary": "暂无数据"}
        rows = []
        for _, r in df.iterrows():
            cap = float(r.get("capital", 0) or 0)
            lia = float(r.get("lia", 0) or 0)
            control = min(100, round(cap * 0.55 + lia * 0.45, 1))
            stability = "高" if control >= 80 else "中" if control >= 65 else "低"
            rotation = "流入" if cap >= 70 else "中性" if cap >= 55 else "流出"
            rows.append({
                "code": r.get("code"),
                "name": r.get("name"),
                "institution_score": round((cap*0.5 + lia*0.5), 1),
                "control": control,
                "stability": stability,
                "rotation": rotation,
                "capital": cap,
            })
        rows = sorted(rows, key=lambda x: x["institution_score"], reverse=True)
        avg = round(sum(x["institution_score"] for x in rows)/len(rows), 1) if rows else 0
        return {"status": "OK", "avg_institution_score": avg, "matrix": rows, "summary": "机构资金矩阵已生成"}
