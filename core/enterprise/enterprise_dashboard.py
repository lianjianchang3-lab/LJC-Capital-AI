from core.commander import CommanderCenter
from core.strategy_v3 import ScoreV3
from core.alerts import AlertCenter

class EnterpriseDashboard:
    def snapshot(self):
        commander = CommanderCenter().snapshot()
        scores = ScoreV3().table()
        alerts = AlertCenter().scan()
        top = []
        if hasattr(scores, "empty") and not scores.empty:
            top = scores.head(5).to_dict("records")
        return {
            "edition": "V8.1 Enterprise",
            "market": commander.get("market", {}),
            "total_position": commander.get("suggested_total_position"),
            "official_status": commander.get("official_status"),
            "alert_count": alerts.get("alert_count"),
            "top_opportunities": top,
            "note": "Enterprise Dashboard：仍基于CSV模式，实盘前必须导入最新数据。",
        }
