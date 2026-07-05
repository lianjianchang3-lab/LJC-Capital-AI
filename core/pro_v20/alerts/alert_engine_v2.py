from datetime import datetime
import pandas as pd
from core.pro_v20.tradeplan.trade_planner_v2 import TradePlannerV2

class AlertEngineV2:
    def __init__(self):
        self.planner = TradePlannerV2()

    def scan(self):
        df = self.planner.plan()
        alerts = []
        if df is None or df.empty:
            return pd.DataFrame()

        for _, r in df.iterrows():
            code = r.get("code")
            name = r.get("name")
            if r.get("最终动作") == "买入关注":
                alerts.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "level": "BUY",
                    "code": code,
                    "name": name,
                    "alert": "AI买入关注",
                    "reason": r.get("交易理由"),
                })
            if r.get("资金共振",0) >= 85:
                alerts.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "level": "CAPITAL",
                    "code": code,
                    "name": name,
                    "alert": "资金共振增强",
                    "reason": r.get("交易理由"),
                })
            if r.get("风险等级") == "高":
                alerts.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "level": "RISK",
                    "code": code,
                    "name": name,
                    "alert": "风险升高",
                    "reason": r.get("交易理由"),
                })
        return pd.DataFrame(alerts)
