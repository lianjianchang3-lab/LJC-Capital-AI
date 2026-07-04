import pandas as pd
from pathlib import Path
from datetime import datetime

class V91RealtimeHub:
    """
    V9.1 实时数据枢纽。
    当前支持：
    1. data/realtime/quotes_realtime.csv
    2. data/inbox/quotes.csv
    3. data/quotes.csv

    预留 AkShare / Tushare / EastMoney / Broker API 接口。
    """
    def __init__(self):
        self.sources = [
            ("Realtime CSV", Path("data/realtime/quotes_realtime.csv")),
            ("Inbox CSV", Path("data/inbox/quotes.csv")),
            ("Local CSV", Path("data/quotes.csv")),
        ]

    def quotes(self):
        for name, path in self.sources:
            if path.exists():
                try:
                    df = pd.read_csv(path)
                    if df.empty:
                        continue
                    if "code" in df.columns:
                        df["code"] = df["code"].astype(str).str.replace(".0","",regex=False).str.zfill(6)
                    df["source"] = name
                    df["loaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    return df
                except Exception:
                    continue
        return pd.DataFrame()

    def health(self):
        rows = []
        active = "WAITING_DATA"
        for name, path in self.sources:
            exists = path.exists()
            n = 0
            updated = None
            if exists:
                try:
                    n = len(pd.read_csv(path))
                    updated = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    if active == "WAITING_DATA" and n > 0:
                        active = name
                except Exception as e:
                    updated = f"ERROR: {e}"
            rows.append({"source": name, "exists": exists, "rows": n, "updated": updated, "path": str(path)})
        return {
            "engine": "V9.1 Realtime Hub",
            "active_source": active,
            "rows": len(self.quotes()),
            "realtime": active == "Realtime CSV",
            "sources": rows,
        }
