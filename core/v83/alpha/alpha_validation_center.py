import pandas as pd
from pathlib import Path
from core.strategy_v3 import ScoreV3

class AlphaValidationCenter:
    """
    M2 Alpha Validation.
    如果存在 data/calibration/history_returns.csv，则计算历史相似验证。
    否则返回当前评分验证卡。
    """
    def __init__(self, history_path="data/calibration/history_returns.csv"):
        self.history_path = Path(history_path)
        self.score = ScoreV3()

    def validate(self):
        score = self.score.table()
        if score.empty:
            return {"status": "NO SCORE DATA", "cards": []}

        cards = []
        hist = None
        if self.history_path.exists():
            hist = pd.read_csv(self.history_path)
            if "code" in hist.columns:
                hist["code"] = hist["code"].astype(str).str.zfill(6)

        for _, r in score.iterrows():
            code = str(r.get("code","")).zfill(6)
            similar_count = 0
            win_rate = None
            avg_return = None
            max_drawdown = None
            confidence = "B"

            if hist is not None and "future_return_20d" in hist.columns:
                rows = hist[hist["code"] == code]
                similar_count = len(rows)
                if similar_count:
                    ret = pd.to_numeric(rows["future_return_20d"], errors="coerce").dropna()
                    if len(ret):
                        win_rate = round(float((ret > 0).mean()), 4)
                        avg_return = round(float(ret.mean()), 4)
                        max_drawdown = round(float(ret.min()), 4)
                        confidence = "A+" if win_rate and win_rate >= 0.75 else "A" if win_rate and win_rate >= 0.60 else "B"

            cards.append({
                "code": code,
                "name": r.get("name",""),
                "investment_score": r.get("investment_score"),
                "lia": r.get("lia"),
                "capital": r.get("capital"),
                "risk": r.get("risk"),
                "suggestion": "BUY/HOLD" if r.get("investment_score",0) >= 85 and r.get("risk",100) < 70 else "WATCH",
                "similar_samples": similar_count,
                "win_rate": win_rate,
                "avg_return_20d": avg_return,
                "max_drawdown": max_drawdown,
                "confidence": confidence,
                "why": f"Score={r.get('investment_score')} Capital={r.get('capital')} Risk={r.get('risk')}",
            })
        return {"status": "OK", "cards": cards}
