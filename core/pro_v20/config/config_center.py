from pathlib import Path
import pandas as pd

class ProConfigCenter:
    def __init__(self):
        self.watchlist_path = Path("config/ljc_watchlist.csv")
        self.weights_path = Path("config/ljc_weights.csv")
        self.holdings_path = Path("data/portfolio/holdings.csv")

    def watchlist(self):
        if self.watchlist_path.exists():
            df = pd.read_csv(self.watchlist_path, dtype={"code": str})
            df["code"] = df["code"].astype(str).str.zfill(6)
            return df
        return pd.DataFrame(columns=["code", "name", "group"])

    def holdings(self):
        if self.holdings_path.exists():
            df = pd.read_csv(self.holdings_path, dtype={"code": str})
            df["code"] = df["code"].astype(str).str.zfill(6)
            for c in ["cost", "shares", "target_weight"]:
                df[c] = pd.to_numeric(df.get(c, 0), errors="coerce").fillna(0)
            return df
        return pd.DataFrame(columns=["code","name","cost","shares","target_weight"])

    def weights(self):
        if self.weights_path.exists():
            df = pd.read_csv(self.weights_path)
            return dict(zip(df["factor"], df["weight"]))
        return {"capital":0.30, "trend":0.25, "volume":0.15, "risk":0.15, "realtime":0.15}
