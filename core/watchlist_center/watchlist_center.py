from pathlib import Path
import pandas as pd


class WatchlistCenter:
    def __init__(self, path="data/watchlist/watchlist.csv"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _code(self, code):
        code = str(code or "").strip().replace(".0", "")
        return code.zfill(6) if code else ""

    def _ensure(self):
        if not self.path.exists():
            pd.DataFrame([
                {"code": "300059", "name": "东方财富", "note": "核心观察"},
                {"code": "688387", "name": "信科移动", "note": "观察"},
                {"code": "688008", "name": "澜起科技", "note": "芯片"},
                {"code": "300762", "name": "上海瀚讯", "note": "商业航天"},
            ]).to_csv(self.path, index=False)

    def list(self):
        self._ensure()
        try:
            df = pd.read_csv(self.path, dtype={"code": str})
        except Exception:
            df = pd.DataFrame(columns=["code", "name", "note"])
        for c in ["code", "name", "note"]:
            if c not in df.columns:
                df[c] = ""
        df["code"] = df["code"].apply(self._code)
        df["name"] = df["name"].fillna("").astype(str).str.strip()
        df["note"] = df["note"].fillna("").astype(str).str.strip()
        df = df[df["code"] != ""].drop_duplicates("code", keep="last")
        return df[["code", "name", "note"]].reset_index(drop=True)

    def save(self, df):
        if df is None:
            df = pd.DataFrame(columns=["code", "name", "note"])
        df = df.copy()
        for c in ["code", "name", "note"]:
            if c not in df.columns:
                df[c] = ""
        df["code"] = df["code"].apply(self._code)
        df["name"] = df["name"].fillna("").astype(str).str.strip()
        df["note"] = df["note"].fillna("").astype(str).str.strip()
        df = df[df["code"] != ""].drop_duplicates("code", keep="last")
        df[["code", "name", "note"]].to_csv(self.path, index=False)
        return df[["code", "name", "note"]].reset_index(drop=True)

    def add(self, code, name="", note=""):
        code = self._code(code)
        if not code:
            return self.list()
        df = self.list()
        df = df[df["code"] != code]
        df = pd.concat([df, pd.DataFrame([{"code": code, "name": str(name or code).strip(), "note": str(note or "").strip()}])], ignore_index=True)
        return self.save(df)

    def remove(self, code):
        code = self._code(code)
        df = self.list()
        df = df[df["code"] != code]
        return self.save(df)

    def analyze(self):
        wl = self.list()
        if wl.empty:
            return wl
        try:
            from core.execution import ExecutionCenter
            exe = ExecutionCenter().dataframe()
        except Exception:
            exe = pd.DataFrame()
        if exe is None or exe.empty or "code" not in exe.columns:
            wl["自选状态"] = "待分析"
            return wl
        exe = exe.copy()
        exe["code"] = exe["code"].apply(self._code)
        df = wl.merge(exe, on="code", how="left", suffixes=("_watch", ""))
        if "name_watch" in df.columns:
            df["name"] = df.get("name", df["name_watch"]).fillna(df["name_watch"])
        df["自选状态"] = "观察"
        if "买入优先级" in df.columns:
            df["买入优先级"] = pd.to_numeric(df["买入优先级"], errors="coerce").fillna(9)
            df.loc[df["买入优先级"] <= 3, "自选状态"] = "重点跟踪"
            df.loc[df["买入优先级"] <= 2, "自选状态"] = "强跟踪"
            df.loc[df["买入优先级"] == 9, "自选状态"] = "暂回避"
        return df

    def summary(self):
        df = self.analyze()
        if df.empty:
            return {"status": "NO DATA", "focus": 0, "avoid": 0, "summary": "暂无自选股"}
        focus = int(df["自选状态"].astype(str).str.contains("重点|强", na=False).sum()) if "自选状态" in df.columns else 0
        avoid = int(df["自选状态"].astype(str).str.contains("回避", na=False).sum()) if "自选状态" in df.columns else 0
        return {"status": "OK", "focus": focus, "avoid": avoid, "summary": f"自选股 {len(df)} 只，重点跟踪 {focus} 只，暂回避 {avoid} 只。"}
