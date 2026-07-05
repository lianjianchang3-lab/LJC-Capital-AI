import time
from pathlib import Path
import pandas as pd

class TTLCache:
    def __init__(self, ttl=10):
        self.ttl = ttl
        self.data = {}

    def get(self, key):
        value = self.data.get(key)
        if value is None:
            return None
        ts, obj = value
        if time.time() - ts > self.ttl:
            self.data.pop(key, None)
            return None
        return obj

    def set(self, key, obj):
        self.data[key] = (time.time(), obj)

class CSVCache:
    def __init__(self, path="data/cache/dataos_market_cache.csv"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, df):
        if df is not None and not df.empty:
            df.to_csv(self.path, index=False)

    def load(self):
        if self.path.exists():
            return pd.read_csv(self.path, dtype={"code": str})
        return pd.DataFrame()
