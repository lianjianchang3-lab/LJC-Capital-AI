from pathlib import Path
import pandas as pd


class DataEngineV33:
    def __init__(self, project_root=None):
        self.root = Path(project_root or Path.cwd())
        self.data_dir = self.root / "data"

    def _read_csv(self, name):
        path = self.data_dir / name
        if not path.exists():
            return pd.DataFrame()
        return pd.read_csv(path, dtype={"code": str})

    def watchlist(self):
        return self._read_csv("watchlist.csv")

    def main_force(self):
        df = self._read_csv("main_force_daily.csv")
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            for col in ["main_force", "super_large", "large_order", "turnover"]:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        return df

    def stock_daily(self):
        df = self._read_csv("stock_daily.csv")
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            for col in ["close", "change_pct", "volume_ratio"]:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        return df
