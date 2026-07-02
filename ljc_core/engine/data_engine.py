from pathlib import Path
import pandas as pd


class DataEngine:
    def __init__(self, project_root=None):
        self.root = Path(project_root or Path.cwd())
        self.data_dirs = [
            self.root / "data",
            self.root / "ljc_core" / "data",
        ]

    def _path(self, name):
        for d in self.data_dirs:
            p = d / name
            if p.exists():
                return p
        return self.data_dirs[0] / name

    def read_csv(self, name):
        path = self._path(name)
        if not path.exists():
            return pd.DataFrame()
        return pd.read_csv(path, dtype={"code": str})

    def watchlist(self):
        return self.read_csv("watchlist.csv")

    def main_force(self):
        df = self.read_csv("main_force_daily.csv")
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            for col in ["main_force", "super_large", "large_order", "turnover"]:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        return df

    def stock_daily(self):
        df = self.read_csv("stock_daily.csv")
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            for col in ["close", "change_pct", "volume_ratio"]:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        return df
