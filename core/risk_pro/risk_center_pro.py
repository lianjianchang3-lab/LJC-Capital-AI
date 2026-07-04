from core.strategy_v3 import ScoreV3
from core.alerts import AlertCenter

class RiskCenterPro:
    def analyze(self):
        df = ScoreV3().table()
        alerts = AlertCenter().scan()
        if df.empty:
            return {"status": "NO DATA", "risk_level": "UNKNOWN", "risk_score": 0, "items": []}
        avg_risk = round(float(df["risk"].mean()), 1) if "risk" in df.columns else 50
        high = df[df["risk"] >= 70].to_dict("records") if "risk" in df.columns else []
        if avg_risk >= 70:
            level = "HIGH"
        elif avg_risk >= 55:
            level = "MEDIUM"
        else:
            level = "LOW"
        return {
            "status": "OK",
            "risk_level": level,
            "risk_score": avg_risk,
            "alert_count": alerts.get("alert_count"),
            "high_risk_positions": high[:10],
            "risk_note": "控制总仓位和单股集中度；当前数据非实时。",
        }
