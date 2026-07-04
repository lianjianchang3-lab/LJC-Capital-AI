import time
from pathlib import Path
import pandas as pd
from core.provider.base_provider import BaseProvider

class CSVProvider(BaseProvider):
    name = "CSV Provider"
    mode = "CSV"

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def _read(self, filename):
        path = self.data_dir / filename
        if not path.exists():
            return pd.DataFrame()
        for enc in ["utf-8-sig", "utf-8", "gbk", "gb18030"]:
            try:
                return pd.read_csv(path, encoding=enc, dtype={"code": str, "代码": str, "证券代码": str})
            except Exception:
                continue
        return pd.DataFrame()

    def _normalize(self, df):
        if df.empty:
            return df
        df = df.copy()
        if "code" not in df.columns:
            for c in ["代码", "证券代码", "股票代码"]:
                if c in df.columns:
                    df["code"] = df[c]
                    break
        if "name" not in df.columns:
            for c in ["名称", "证券名称", "股票名称"]:
                if c in df.columns:
                    df["name"] = df[c]
                    break
        if "code" in df.columns:
            df["code"] = df["code"].astype(str).str.replace(".0", "", regex=False).str.zfill(6)
        return df

    def get_quotes(self): return self._normalize(self._read("quotes.csv"))
    def get_capital(self): return self._normalize(self._read("capital.csv"))
    def get_portfolio(self): return self._normalize(self._read("portfolio.csv"))

    def health(self):
        start = time.time()
        q = self.get_quotes()
        c = self.get_capital()
        latency = int((time.time() - start) * 1000)
        return {"provider": self.name, "mode": self.mode, "ready": not q.empty, "latency_ms": latency, "message": f"quotes={len(q)}, capital={len(c)}" if not q.empty else "quotes.csv missing or unreadable"}
