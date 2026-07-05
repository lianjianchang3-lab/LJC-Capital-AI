from pathlib import Path
from datetime import datetime
import pandas as pd

class TradeLogbook:
    def __init__(self):
        self.path = Path("data/trading/trade_log.csv")
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def ensure(self):
        if not self.path.exists():
            pd.DataFrame(columns=[
                "time","code","name","action","price","shares","reason","ai_score","status"
            ]).to_csv(self.path, index=False)

    def read(self):
        self.ensure()
        return pd.read_csv(self.path, dtype={"code": str})

    def add_ai_snapshot(self):
        from core.pro_v20.tradeplan.trade_planner_v2 import TradePlannerV2
        df = TradePlannerV2().plan()
        if df is None or df.empty:
            return 0
        log = self.read()
        rows = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for _, r in df.head(10).iterrows():
            rows.append({
                "time": now,
                "code": r.get("code"),
                "name": r.get("name"),
                "action": r.get("最终动作"),
                "price": r.get("price"),
                "shares": 0,
                "reason": r.get("交易理由"),
                "ai_score": r.get("Alpha2.0"),
                "status": "AI建议记录",
            })
        out = pd.concat([log, pd.DataFrame(rows)], ignore_index=True)
        out.to_csv(self.path, index=False)
        return len(rows)
