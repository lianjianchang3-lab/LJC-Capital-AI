from pathlib import Path
from datetime import datetime
import pandas as pd
from core.pro_v40.engine.unified_ai_engine import UnifiedAIEngine

class LearningCenter:
    def __init__(self):
        self.path = Path("data/learning/ai_recommendation_log.csv")
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _ensure(self):
        if not self.path.exists():
            pd.DataFrame(columns=[
                "time","code","name","ai_score","recommendation","price","evidence","result_1d","result_5d","status"
            ]).to_csv(self.path, index=False)

    def read(self):
        self._ensure()
        return pd.read_csv(self.path, dtype={"code":str})

    def snapshot(self):
        self._ensure()
        old = self.read()
        df = UnifiedAIEngine().run()
        if df.empty:
            return 0
        rows = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for _, r in df.head(10).iterrows():
            rows.append({
                "time": now,
                "code": r.get("code"),
                "name": r.get("name"),
                "ai_score": r.get("Unified AI Score"),
                "recommendation": r.get("统一建议"),
                "price": r.get("price"),
                "evidence": r.get("证据链"),
                "result_1d": "",
                "result_5d": "",
                "status": "待验证",
            })
        out = pd.concat([old, pd.DataFrame(rows)], ignore_index=True)
        out.to_csv(self.path, index=False)
        return len(rows)

    def stats(self):
        df = self.read()
        total = len(df)
        verified = df[df["status"].isin(["成功","失败"])] if "status" in df.columns else pd.DataFrame()
        success = int((verified["status"]=="成功").sum()) if not verified.empty else 0
        rate = round(success/len(verified)*100,1) if len(verified)>0 else 0
        return {"total": total, "verified": len(verified), "success": success, "success_rate": rate}
