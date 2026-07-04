import pandas as pd
from pathlib import Path
from datetime import datetime

class RealtimeProvider:
    """
    V8.2 realtime provider adapter.
    当前先支持 data/realtime/quotes_realtime.csv。
    以后可替换为 Tushare / AkShare / 券商 / WebSocket。
    """
    def __init__(self, path="data/realtime/quotes_realtime.csv"):
        self.path = Path(path)

    def available(self):
        return self.path.exists()

    def get_quotes(self):
        if not self.available():
            return pd.DataFrame()
        df = pd.read_csv(self.path)
        if "code" in df.columns:
            df["code"] = df["code"].astype(str).str.zfill(6)
        return df

    def status(self):
        return {
            "provider": "Realtime CSV Adapter",
            "available": self.available(),
            "path": str(self.path),
            "updated": datetime.fromtimestamp(self.path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S") if self.available() else None,
            "mode": "REALTIME_ADAPTER" if self.available() else "WAITING_DATA",
        }

class RealtimeProviderManager:
    def __init__(self):
        self.provider = RealtimeProvider()

    def snapshot(self):
        return {
            "status": self.provider.status(),
            "rows": len(self.provider.get_quotes()),
        }
