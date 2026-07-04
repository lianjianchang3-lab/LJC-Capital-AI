from pathlib import Path
from datetime import datetime
from core.v92.live import V92LiveDataEngine

class V92RefreshCenter:
    def refresh_to_csv(self):
        df = V92LiveDataEngine().get_quotes(prefer_live=True)
        Path("data/realtime").mkdir(parents=True, exist_ok=True)
        out = Path("data/realtime/quotes_realtime.csv")
        if df.empty:
            return {"status": "NO DATA", "path": str(out), "rows": 0}
        df.to_csv(out, index=False)
        return {
            "status": "OK",
            "path": str(out),
            "rows": len(df),
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": df["source"].iloc[0] if "source" in df.columns else "unknown",
        }
