from pathlib import Path
from datetime import datetime
import pandas as pd
from core.pro_v20.trading import TradePlanEngine

class ReviewCenter:
    def __init__(self):
        self.path = Path("data/review/decision_journal.csv")

    def snapshot(self):
        df = TradePlanEngine().plans()
        if df.empty:
            return pd.DataFrame()
        out = df.copy()
        out["snapshot_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Path("data/review").mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            old = pd.read_csv(self.path)
            out = pd.concat([old, out], ignore_index=True)
        out.to_csv(self.path, index=False)
        return out.tail(len(df))

    def summary(self):
        if not self.path.exists():
            return {"records":0, "summary":"暂无复盘记录"}
        df = pd.read_csv(self.path)
        return {"records":len(df), "summary":f"已记录 {len(df)} 条AI建议，可用于后续命中率复盘"}
