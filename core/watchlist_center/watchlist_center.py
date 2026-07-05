from pathlib import Path
import pandas as pd


class WatchlistCenter:
    """
    V8.5 Build002 自选股中心。
    默认读取 config/ljc_watchlist.csv；没有则读取 data/watchlist/watchlist.csv。
    """

    def __init__(self, path="config/ljc_watchlist.csv"):
        self.path = Path(path)
        self.fallback = Path("data/watchlist/watchlist.csv")

    def _ensure(self):
        self.fallback.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists() and not self.fallback.exists():
            pd.DataFrame([
                {"code": "300059", "name": "东方财富"},
                {"code": "688387", "name": "信科移动"},
                {"code": "688008", "name": "澜起科技"},
                {"code": "300762", "name": "上海瀚讯"},
            ]).to_csv(self.fallback, index=False)

    def list(self):
        self._ensure()
        p = self.path if self.path.exists() else self.fallback
        try:
            df = pd.read_csv(p, dtype={"code": str})
        except Exception:
            return pd.DataFrame()
        if df.empty:
            return df
        df["code"] = df["code"].astype(str).str.replace(".0", "", regex=False).str.zfill(6)
        if "name" not in df.columns:
            df["name"] = df["code"]
        return df

    def analyze(self):
        wl = self.list()
        if wl.empty:
            return pd.DataFrame()

        from core.execution import ExecutionCenter
        exe = ExecutionCenter().dataframe()
        if exe is None or exe.empty:
            return wl

        exe = exe.copy()
        exe["code"] = exe["code"].astype(str).str.zfill(6)
        df = wl.merge(exe, on="code", how="left", suffixes=("_watch", ""))
        if "name" not in df.columns and "name_watch" in df.columns:
            df["name"] = df["name_watch"]
        df["自选状态"] = "观察"
        if "买入优先级" in df.columns:
            df.loc[df["买入优先级"] <= 3, "自选状态"] = "重点跟踪"
            df.loc[df["买入优先级"] <= 2, "自选状态"] = "强跟踪"
            df.loc[df["买入优先级"] == 9, "自选状态"] = "暂回避"
        return df

    def summary(self):
        df = self.analyze()
        if df.empty:
            return {"status": "NO DATA", "summary": "暂无自选股"}
        focus = int(df["自选状态"].astype(str).str.contains("重点|强", na=False).sum())
        avoid = int(df["自选状态"].astype(str).str.contains("回避", na=False).sum())
        return {"status": "OK", "focus": focus, "avoid": avoid, "summary": f"自选股 {len(df)} 只，重点跟踪 {focus} 只，暂回避 {avoid} 只。"}
