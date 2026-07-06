from pathlib import Path
import json
import time
import pandas as pd


class OfflineCache:
    """
    V8.5 Build006 离线缓存层。
    目标：早上开盘前手机必须能打开，不被 AkShare / 东方财富接口卡死。
    """

    def __init__(self, cache_dir="data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, name):
        return self.cache_dir / name

    def read_json(self, name, default=None):
        p = self._path(name)
        if not p.exists():
            return default
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return default

    def write_json(self, name, data):
        p = self._path(name)
        payload = {"updated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "data": data}
        p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return payload

    def read_csv(self, name, default=None):
        p = self._path(name)
        if not p.exists():
            return default if default is not None else pd.DataFrame()
        try:
            return pd.read_csv(p, dtype={"code": str})
        except Exception:
            return default if default is not None else pd.DataFrame()

    def write_csv(self, name, df):
        p = self._path(name)
        df.to_csv(p, index=False)
        return str(p)

    def status(self):
        files = []
        for p in sorted(self.cache_dir.glob("*")):
            try:
                files.append({"file": p.name, "size": p.stat().st_size, "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.stat().st_mtime))})
            except Exception:
                pass
        return files
