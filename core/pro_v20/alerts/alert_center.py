from datetime import datetime
import pandas as pd
from pathlib import Path
from core.pro_v20.trading import TradePlanEngine

class AlertCenter:
    def __init__(self):
        self.engine = TradePlanEngine()
        self.log_path = Path("data/alerts/alerts_log.csv")

    def generate(self):
        df = self.engine.plans()
        alerts = []
        if df.empty:
            return []

        for _, r in df.iterrows():
            score = float(r.get("LJC Alpha Score", 0) or 0)
            action = r.get("交易动作", "")
            pct = float(r.get("change_pct", 0) or 0)
            code = r.get("code")
            name = r.get("name")
            if action == "买入/加仓":
                alerts.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "level": "HIGH", "code": code, "name": name, "alert": "AI买入/加仓信号", "reason": f"Alpha {score}，动作 {action}"})
            if action == "减仓/止损":
                alerts.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "level": "RISK", "code": code, "name": name, "alert": "AI风险/减仓信号", "reason": f"涨跌幅 {pct}%，动作 {action}"})
            if pct >= 8:
                alerts.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "level": "WATCH", "code": code, "name": name, "alert": "强势异动", "reason": f"涨幅 {pct}%"})
        return alerts

    def save(self):
        alerts = self.generate()
        if alerts:
            Path("data/alerts").mkdir(parents=True, exist_ok=True)
            df = pd.DataFrame(alerts)
            if self.log_path.exists():
                old = pd.read_csv(self.log_path)
                df = pd.concat([old, df], ignore_index=True)
            df.to_csv(self.log_path, index=False)
        return alerts
