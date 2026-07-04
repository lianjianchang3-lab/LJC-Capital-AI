import pandas as pd
from pathlib import Path
from core.strategy_v3 import ScoreV3

class ModelCalibrator:
    """
    校准评分模型：
    需要 data/calibration/history_returns.csv
    columns: code, future_return_5d, future_return_20d
    """
    def __init__(self, path="data/calibration/history_returns.csv"):
        self.path = Path(path)

    def run(self):
        score = ScoreV3().table()
        if score.empty:
            return {"status": "NO SCORE DATA", "metrics": {}, "table": []}
        if not self.path.exists():
            return {
                "status": "WAITING_HISTORY_RETURNS",
                "metrics": {},
                "table": score.head(10).to_dict("records"),
                "instruction": "请准备 data/calibration/history_returns.csv，包含 code,future_return_5d,future_return_20d",
            }
        hist = pd.read_csv(self.path)
        hist["code"] = hist["code"].astype(str).str.zfill(6)
        merged = score.merge(hist, on="code", how="inner")
        if merged.empty:
            return {"status": "NO MATCHED DATA", "metrics": {}, "table": []}

        metrics = {}
        for col in ["future_return_5d", "future_return_20d"]:
            if col in merged.columns:
                corr = merged["investment_score"].corr(pd.to_numeric(merged[col], errors="coerce"))
                metrics[f"corr_score_{col}"] = round(float(corr), 4) if pd.notna(corr) else None

        merged["score_bucket"] = pd.cut(
            merged["investment_score"],
            bins=[0, 60, 70, 80, 90, 100],
            labels=["D", "C", "B", "A", "A+"],
            include_lowest=True,
        )
        return {
            "status": "OK",
            "metrics": metrics,
            "bucket_summary": merged.groupby("score_bucket", observed=False)[["future_return_5d","future_return_20d"]].mean(numeric_only=True).reset_index().to_dict("records"),
            "table": merged.to_dict("records"),
        }
