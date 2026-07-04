import json
from pathlib import Path
from datetime import datetime
from core.v83.alpha import AlphaValidationCenter

class LearningEngine:
    """
    M3 AI Learning Engine.
    根据 Alpha Validation 的历史表现生成建议权重。
    """
    def __init__(self, model_dir="data/v83/models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)

    def calibrate(self):
        result = AlphaValidationCenter().validate()
        cards = result.get("cards", [])
        weights = {"trend": 0.25, "capital": 0.30, "quality": 0.15, "risk": 0.30}
        valid = [c for c in cards if c.get("win_rate") is not None]
        if valid:
            avg_win = sum(c["win_rate"] for c in valid) / len(valid)
            if avg_win >= 0.65:
                weights = {"trend": 0.22, "capital": 0.36, "quality": 0.14, "risk": 0.28}
            else:
                weights = {"trend": 0.28, "capital": 0.26, "quality": 0.16, "risk": 0.30}
        model = {
            "version": datetime.now().strftime("v83-%Y%m%d-%H%M%S"),
            "weights": weights,
            "sample_count": len(valid),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "note": "自动校准建议；人工确认后再用于实盘。",
        }
        path = self.model_dir / "latest_model.json"
        path.write_text(json.dumps(model, ensure_ascii=False, indent=2), encoding="utf-8")
        return model

    def latest(self):
        path = self.model_dir / "latest_model.json"
        if not path.exists():
            return {"status": "NO MODEL", "message": "请先运行 calibrate"}
        return json.loads(path.read_text(encoding="utf-8"))
