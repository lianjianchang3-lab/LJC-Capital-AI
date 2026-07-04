from datetime import datetime
from pathlib import Path
import json
from core.v93.scanner import V93MarketScanner

class V93SignalEngine:
    def generate(self):
        scan = V93MarketScanner().scan(top_n=100)
        signals = []
        for item in scan.get("items", []):
            if item.get("decision") in ["BUY", "WATCH_BUY", "RISK_ALERT"]:
                signals.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "code": item.get("code"),
                    "name": item.get("name"),
                    "decision": item.get("decision"),
                    "position": item.get("position"),
                    "ai_score_v3": item.get("ai_score_v3"),
                    "price": item.get("price"),
                    "change_pct": item.get("change_pct"),
                    "reason": item.get("reason"),
                })
        Path("logs").mkdir(exist_ok=True)
        Path("logs/v93_latest_signals.json").write_text(json.dumps(signals, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": scan.get("status"), "summary": scan.get("summary"), "signals": signals}
