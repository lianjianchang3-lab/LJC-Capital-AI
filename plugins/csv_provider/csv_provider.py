from pathlib import Path
import pandas as pd
from core.data_center.schema import DataQuality, DataResult


class CSVProvider:
    name = "csv"

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)

    def _read(self, filename: str):
        path = self.data_dir / filename
        if not path.exists():
            return pd.DataFrame(), DataQuality(self.name, 0, "missing", f"{filename} not found")
        try:
            df = pd.read_csv(path, dtype={"code": str})
            return df, DataQuality(self.name, 80, "ok", f"{filename} loaded")
        except Exception as e:
            return pd.DataFrame(), DataQuality(self.name, 0, "error", str(e))

    def fetch_watchlist(self):
        df, q = self._read("watchlist.csv")
        return DataResult(df, q)

    def fetch_quotes(self, symbols=None):
        df, q = self._read("quotes.csv")
        if symbols and not df.empty and "code" in df.columns:
            symbols = [str(s).zfill(6) for s in symbols]
            df = df[df["code"].astype(str).str.zfill(6).isin(symbols)]
        return DataResult(df, q)

    def fetch_capital(self, symbols=None):
        df, q = self._read("capital.csv")
        if symbols and not df.empty and "code" in df.columns:
            symbols = [str(s).zfill(6) for s in symbols]
            df = df[df["code"].astype(str).str.zfill(6).isin(symbols)]
        return DataResult(df, q)

    def fetch_sector(self):
        df, q = self._read("sector.csv")
        return DataResult(df, q)

    def fetch_news(self, symbols=None):
        df, q = self._read("news.csv")
        if symbols and not df.empty and "code" in df.columns:
            symbols = [str(s).zfill(6) for s in symbols]
            df = df[df["code"].astype(str).str.zfill(6).isin(symbols)]
        return DataResult(df, q)
