from pathlib import Path
from datetime import datetime
import pandas as pd

class V90RealtimeManager:
    """
    V9.0 实时数据总线。
    优先级：
    1. data/realtime/quotes_realtime.csv
    2. data/inbox/quotes.csv
    3. data/quotes.csv
    """
    def __init__(self):
        self.sources = [
            ("Realtime CSV", Path("data/realtime/quotes_realtime.csv")),
            ("Inbox CSV", Path("data/inbox/quotes.csv")),
            ("Local CSV", Path("data/quotes.csv")),
        ]

    def _read(self, path):
        df = pd.read_csv(path)
        if "code" in df.columns:
            df["code"] = df["code"].astype(str).str.replace(".0", "", regex=False).str.zfill(6)
        return df

    def get_quotes(self):
        for name, path in self.sources:
            if path.exists():
                df = self._read(path)
                if not df.empty:
                    df["source"] = name
                    return df
        return pd.DataFrame()

    def health(self):
        rows = []
        active = None
        active_rows = 0
        for name, path in self.sources:
            exists = path.exists()
            count = 0
            updated = None
            if exists:
                try:
                    count = len(pd.read_csv(path))
                    updated = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    updated = f"ERROR: {e}"
            rows.append({"source": name, "path": str(path), "exists": exists, "rows": count, "updated": updated})
            if active is None and exists and count > 0:
                active = name
                active_rows = count
        return {
            "engine": "V9.0 Realtime Data Bus",
            "active_source": active or "WAITING_DATA",
            "active_rows": active_rows,
            "realtime_ready": active == "Realtime CSV",
            "sources": rows,
        }
