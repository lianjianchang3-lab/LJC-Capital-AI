from pathlib import Path
from datetime import datetime, date
import pandas as pd


class DataStatusCenter:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)

    def _read(self, name):
        path = self.data_dir / name
        if not path.exists():
            return pd.DataFrame(), None
        try:
            df = pd.read_csv(path, dtype={"code": str, "代码": str, "证券代码": str})
            return df, path
        except Exception:
            return pd.DataFrame(), path

    def _pick_date(self, df):
        if df.empty:
            return None
        for col in ["date", "日期", "交易日期", "timestamp", "time", "更新时间"]:
            if col in df.columns:
                series = df[col].dropna()
                if not series.empty:
                    value = str(series.iloc[-1])
                    return value[:10]
        return None

    def _file_mtime(self, path):
        if not path:
            return None
        return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")

    def status(self):
        quotes, qpath = self._read("quotes.csv")
        capital, cpath = self._read("capital.csv")

        quote_date = self._pick_date(quotes)
        capital_date = self._pick_date(capital)
        data_date = quote_date or capital_date
        today = date.today().strftime("%Y-%m-%d")

        provider = "CSV Import"
        mode = "CSV TEST MODE"
        source = "CSV Local"
        realtime = False

        freshness = "UNKNOWN"
        stale = True
        if data_date:
            if data_date == today:
                freshness = "TODAY"
                stale = False
            else:
                freshness = "STALE"
                stale = True

        updated_at = self._file_mtime(qpath) or self._file_mtime(cpath) or "N/A"

        health = 100
        issues = []

        if quotes.empty:
            health -= 30
            issues.append("行情CSV缺失")
        if capital.empty:
            health -= 25
            issues.append("资金CSV缺失")
        if stale:
            health -= 25
            issues.append("数据不是今日实时数据")
        if source == "CSV Local":
            health -= 10
            issues.append("当前为CSV测试模式，非实时行情")

        return {
            "source": source,
            "provider": provider,
            "mode": mode,
            "realtime": realtime,
            "data_date": data_date or "无法识别",
            "today": today,
            "updated_at": updated_at,
            "freshness": freshness,
            "stale": stale,
            "latency": "N/A",
            "health": max(0, health),
            "issues": issues,
            "quote_rows": len(quotes),
            "capital_rows": len(capital),
            "warning": "当前不是实时行情，不能直接作为实盘交易依据。" if source == "CSV Local" else "",
        }

    def is_live(self):
        s = self.status()
        return s["realtime"] is True and s["stale"] is False
