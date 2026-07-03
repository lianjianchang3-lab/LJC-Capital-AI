from pathlib import Path
from datetime import datetime
import pandas as pd

from core.gateway.schema import Quote, Capital


class DataGateway:
    """
    V8 Final 统一数据网关。
    所有 AI / Dashboard 只允许从这里获取 Quote / Capital / Portfolio。
    """

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def _read_csv(self, name):
        path = self.data_dir / name
        if not path.exists():
            return pd.DataFrame()
        return pd.read_csv(path, dtype={"code": str, "代码": str, "证券代码": str})

    def _pick(self, row, names, default=None):
        for n in names:
            if n in row:
                return row.get(n)
        return default

    def _num(self, value, default=0.0):
        try:
            if pd.isna(value):
                return default
            s = str(value).replace(",", "").replace("%", "").replace("亿", "").strip()
            if s in ["", "-", "--", "nan", "None"]:
                return default
            if "万" in s:
                return float(s.replace("万", "")) / 10000
            return float(s)
        except Exception:
            return default

    def watchlist(self):
        df = self._read_csv("watchlist.csv")
        if df.empty:
            return pd.DataFrame([
                {"code": "300136", "name": "信维通信", "theme": "AI终端/卫星通信"},
                {"code": "300762", "name": "上海瀚讯", "theme": "商业航天/军工通信"},
                {"code": "688008", "name": "澜起科技", "theme": "AI基础设施/半导体"},
                {"code": "603308", "name": "应流股份", "theme": "高端制造/商业航天"},
                {"code": "688387", "name": "信科移动", "theme": "卫星通信"},
            ])
        if "代码" in df.columns and "code" not in df.columns:
            df["code"] = df["代码"]
        if "名称" in df.columns and "name" not in df.columns:
            df["name"] = df["名称"]
        return df

    def quotes(self):
        df = self._read_csv("quotes.csv")
        rows = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if df.empty:
            for _, r in self.watchlist().iterrows():
                rows.append(Quote(str(r["code"]).zfill(6), r.get("name", ""), 0, 0, 0, now, "missing"))
            return rows

        for _, r in df.iterrows():
            code = str(self._pick(r, ["code", "代码", "证券代码"], "")).zfill(6)
            name = self._pick(r, ["name", "名称", "证券名称"], code)
            price = self._num(self._pick(r, ["close", "最新价", "现价", "price"], 0))
            change_pct = self._num(self._pick(r, ["change_pct", "涨跌幅", "涨幅"], 0))
            turnover = self._num(self._pick(r, ["turnover", "成交额", "成交金额"], 0))
            ts = str(self._pick(r, ["timestamp", "time", "date"], now))
            provider = str(self._pick(r, ["provider", "source"], "csv"))
            rows.append(Quote(code, name, price, change_pct, turnover, ts, provider))
        return rows

    def capital(self):
        df = self._read_csv("capital.csv")
        rows = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if df.empty:
            for _, r in self.watchlist().iterrows():
                rows.append(Capital(str(r["code"]).zfill(6), r.get("name", ""), 0, 0, 0, 0, 0, now, "missing"))
            return rows

        for _, r in df.iterrows():
            code = str(self._pick(r, ["code", "代码", "证券代码"], "")).zfill(6)
            name = self._pick(r, ["name", "名称", "证券名称"], code)
            super_large = self._num(self._pick(r, ["super_large", "超大单", "特大单"], 0))
            large = self._num(self._pick(r, ["large", "大单"], 0))
            medium = self._num(self._pick(r, ["medium", "中单"], 0))
            small = self._num(self._pick(r, ["small", "小单"], 0))
            main = self._num(self._pick(r, ["net_main", "主力净流入", "主力净额"], super_large + large))
            ts = str(self._pick(r, ["timestamp", "time", "date"], now))
            provider = str(self._pick(r, ["provider", "source"], "csv"))
            rows.append(Capital(code, name, main, super_large, large, medium, small, ts, provider))
        return rows

    def portfolio(self):
        return self._read_csv("portfolio.csv")

    def health(self):
        qs = self.quotes()
        cs = self.capital()
        score = 100
        issues = []
        if not qs or all(q.provider == "missing" for q in qs):
            score -= 30
            issues.append("行情数据缺失")
        if not cs or all(c.provider == "missing" for c in cs):
            score -= 25
            issues.append("资金数据缺失")
        return {
            "score": max(0, score),
            "issues": issues,
            "quote_count": len(qs),
            "capital_count": len(cs),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
