from pathlib import Path
import pandas as pd


class DataEngine:
    def __init__(self, project_root=None):
        self.root = Path(project_root or Path.cwd())
        self.data_dirs = [self.root / "data", self.root / "ljc_core" / "data"]

    def _path(self, name):
        for d in self.data_dirs:
            p = d / name
            if p.exists():
                return p
        return self.data_dirs[0] / name

    def read_csv(self, name):
        p = self._path(name)
        if not p.exists():
            return pd.DataFrame()
        return pd.read_csv(p, dtype={"code": str})

    def watchlist(self): return self.read_csv("watchlist.csv")
    def portfolio(self): return self.read_csv("portfolio.csv")

    def main_force(self):
        df = self.read_csv("main_force_daily.csv")
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            for c in ["main_force","super_large","large_order","turnover"]:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        return df

    def stock_daily(self):
        df = self.read_csv("stock_daily.csv")
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            for c in ["close","change_pct","volume_ratio"]:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        return df

    def status(self):
        files = ["watchlist.csv", "main_force_daily.csv", "stock_daily.csv", "portfolio.csv"]
        return [{"file": f, "exists": self._path(f).exists(), "path": str(self._path(f))} for f in files]
