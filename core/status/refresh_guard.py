from pathlib import Path
from datetime import datetime, date
import pandas as pd


class DataRefreshGuard:
    def __init__(self, data_dir="data", inbox_dir="data/inbox"):
        self.data_dir = Path(data_dir)
        self.inbox_dir = Path(inbox_dir)
        self.inbox_dir.mkdir(parents=True, exist_ok=True)

    def file_status(self, filename):
        path = self.data_dir / filename
        if not path.exists():
            return {
                "file": filename,
                "exists": False,
                "rows": 0,
                "mtime": "N/A",
                "date": "无法识别",
                "is_today": False,
                "needs_update": True,
            }

        try:
            df = pd.read_csv(path, dtype={"code": str, "代码": str, "证券代码": str})
        except Exception:
            return {
                "file": filename,
                "exists": True,
                "rows": 0,
                "mtime": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "date": "读取失败",
                "is_today": False,
                "needs_update": True,
            }

        data_date = self._detect_date(df)
        today = date.today().strftime("%Y-%m-%d")
        is_today = data_date == today
        return {
            "file": filename,
            "exists": True,
            "rows": len(df),
            "mtime": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "date": data_date or "无法识别",
            "is_today": is_today,
            "needs_update": not is_today,
        }

    def _detect_date(self, df):
        for col in ["date", "日期", "交易日期", "timestamp", "time", "更新时间"]:
            if col in df.columns:
                s = df[col].dropna()
                if not s.empty:
                    return str(s.iloc[-1])[:10]
        return None

    def all_status(self):
        files = ["quotes.csv", "capital.csv", "portfolio.csv"]
        rows = [self.file_status(f) for f in files]
        return {
            "files": rows,
            "needs_update": any(r["needs_update"] for r in rows if r["file"] in ["quotes.csv", "capital.csv"]),
            "inbox_files": [p.name for p in self.inbox_dir.glob("*.csv")],
        }

    def message(self):
        s = self.all_status()
        if s["needs_update"]:
            return "需要更新数据：quotes.csv 或 capital.csv 不是今日数据。"
        return "数据日期通过今日校验。"
