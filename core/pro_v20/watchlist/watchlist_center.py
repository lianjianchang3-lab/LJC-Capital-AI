import pandas as pd
from core.pro_v20.config.config_center import ProConfigCenter
from core.pro_v20.decision.decision_center import ProDecisionCenter

class ProWatchlistCenter:
    def __init__(self):
        self.config = ProConfigCenter()
        self.decision = ProDecisionCenter()

    def analyze(self):
        watch = self.config.watchlist()
        dec = self.decision.decisions()
        if watch.empty:
            return pd.DataFrame()
        if dec.empty:
            return watch
        if "code" in dec.columns:
            dec["code"] = dec["code"].astype(str).str.zfill(6)
        out = watch.merge(dec, on="code", how="left", suffixes=("_watch", ""))
        if "name" not in out.columns and "name_watch" in out.columns:
            out["name"] = out["name_watch"]
        return out.sort_values("LJC Alpha Score", ascending=False, na_position="last")
