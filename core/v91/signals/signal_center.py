from datetime import datetime
from pathlib import Path
import json
from core.v91.scanner import V91AutoScanner

class V91SignalCenter:
    def generate(self):
        scan = V91AutoScanner().scan()
        items = scan.get("items", [])
        signals = []
        for x in items:
            if x.get("signal") in ["BUY","RISK_ALERT","AVOID"]:
                signals.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "code": x.get("code"),
                    "name": x.get("name"),
                    "signal": x.get("signal"),
                    "score": x.get("scan_score"),
                    "price": x.get("price"),
                    "reason": f"scan={x.get('scan_score')} capital={x.get('capital')} lia={x.get('lia')} risk={x.get('risk')}",
                })
        Path("logs").mkdir(exist_ok=True)
        Path("logs/v91_latest_signals.json").write_text(json.dumps(signals, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"status": scan.get("status"), "summary": scan.get("summary"), "signals": signals}
