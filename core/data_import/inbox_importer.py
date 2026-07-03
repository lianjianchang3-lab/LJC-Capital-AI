from pathlib import Path
from datetime import datetime
import shutil
import pandas as pd


class InboxImporter:
    """
    V8 RC1 Real Data Inbox

    把每天导出的同花顺 / Moomoo / 普通CSV 放到 data/inbox/
    系统自动识别并写入标准文件：
    - data/quotes.csv
    - data/capital.csv
    - data/portfolio.csv
    """

    def __init__(self, inbox="data/inbox", data_dir="data", processed="data/processed"):
        self.inbox = Path(inbox)
        self.data_dir = Path(data_dir)
        self.processed = Path(processed)
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.processed.mkdir(parents=True, exist_ok=True)

    def _read_csv(self, path: Path):
        encodings = ["utf-8-sig", "utf-8", "gbk", "gb18030"]
        last_error = None
        for enc in encodings:
            try:
                return pd.read_csv(path, encoding=enc, dtype={"code": str, "代码": str, "证券代码": str})
            except Exception as e:
                last_error = e
        raise last_error


    def _num(self, value):
        try:
            if value is None:
                return 0.0
            s = str(value).strip().replace(",", "").replace("，", "")
            if s in ["", "-", "--", "nan", "None"]:
                return 0.0
            s = s.replace("%", "")
            unit = 1.0
            if "亿" in s:
                unit = 1.0
                s = s.replace("亿", "")
            elif "万" in s:
                unit = 0.0001
                s = s.replace("万", "")
            return float(s) * unit
        except Exception:
            return 0.0

    def _normalize_code(self, s):
        return str(s).replace(".SZ", "").replace(".SH", "").replace("SZ", "").replace("SH", "").zfill(6)

    def _pick(self, df, candidates):
        for c in candidates:
            if c in df.columns:
                return c
        return None

    def detect_type(self, df, filename):
        cols = set(df.columns)
        lower = filename.lower()

        if "portfolio" in lower or "持仓" in lower:
            return "portfolio"

        if any(c in cols for c in ["super_large", "特大单", "超大单", "主力净流入", "net_main"]):
            return "capital"

        if any(c in cols for c in ["最新价", "现价", "close", "涨跌幅", "change_pct"]):
            return "quotes"

        return "unknown"

    def normalize_quotes(self, df):
        code_col = self._pick(df, ["code", "代码", "证券代码"])
        name_col = self._pick(df, ["name", "名称", "证券名称"])
        close_col = self._pick(df, ["close", "最新价", "现价", "收盘价", "最新", "价格"])
        chg_col = self._pick(df, ["change_pct", "涨跌幅", "涨幅", "涨跌幅(%)"])
        vr_col = self._pick(df, ["volume_ratio", "量比", "量比指标"])
        turnover_col = self._pick(df, ["turnover", "成交额", "成交额(亿)", "成交金额"])

        rows = []
        today = datetime.now().strftime("%Y-%m-%d")
        for _, r in df.iterrows():
            if not code_col:
                continue
            rows.append({
                "date": today,
                "code": self._normalize_code(r.get(code_col, "")),
                "name": r.get(name_col, "") if name_col else "",
                "close": r.get(close_col, 0) if close_col else 0,
                "change_pct": r.get(chg_col, 0) if chg_col else 0,
                "volume_ratio": r.get(vr_col, 1) if vr_col else 1,
                "turnover": r.get(turnover_col, 0) if turnover_col else 0,
            })
        return pd.DataFrame(rows)

    def normalize_capital(self, df):
        code_col = self._pick(df, ["code", "代码", "证券代码"])
        name_col = self._pick(df, ["name", "名称", "证券名称"])
        super_col = self._pick(df, ["super_large", "特大单", "超大单", "超大单净额", "特大单净额", "Super Large"])
        large_col = self._pick(df, ["large", "大单", "大单净额", "Large"])
        medium_col = self._pick(df, ["medium", "中单", "中单净额", "Medium"])
        small_col = self._pick(df, ["small", "小单", "小单净额", "Small"])
        net_col = self._pick(df, ["net_main", "主力净流入", "主力净额", "主力资金净流入", "主力净流入(亿)", "Main Net"])

        rows = []
        today = datetime.now().strftime("%Y-%m-%d")
        for _, r in df.iterrows():
            if not code_col:
                continue
            super_large = self._num(r.get(super_col, 0)) if super_col else 0
            large = self._num(r.get(large_col, 0)) if large_col else 0
            medium = self._num(r.get(medium_col, 0)) if medium_col else 0
            small = self._num(r.get(small_col, 0)) if small_col else 0
            net_main = self._num(r.get(net_col, 0)) if net_col else super_large + large

            rows.append({
                "date": today,
                "source": "inbox",
                "code": self._normalize_code(r.get(code_col, "")),
                "name": r.get(name_col, "") if name_col else "",
                "super_large": super_large if pd.notna(super_large) else 0,
                "large": large if pd.notna(large) else 0,
                "medium": medium if pd.notna(medium) else 0,
                "small": small if pd.notna(small) else 0,
                "net_main": net_main if pd.notna(net_main) else 0,
            })
        return pd.DataFrame(rows)

    def normalize_portfolio(self, df):
        code_col = self._pick(df, ["code", "代码", "证券代码"])
        name_col = self._pick(df, ["name", "名称", "证券名称"])
        shares_col = self._pick(df, ["shares", "持仓", "持股数量", "数量"])
        cost_col = self._pick(df, ["cost", "成本", "成本价", "平均成本"])

        rows = []
        for _, r in df.iterrows():
            if not code_col:
                continue
            rows.append({
                "code": self._normalize_code(r.get(code_col, "")),
                "name": r.get(name_col, "") if name_col else "",
                "shares": r.get(shares_col, 0) if shares_col else 0,
                "cost": r.get(cost_col, 0) if cost_col else 0,
            })
        return pd.DataFrame(rows)

    def import_all(self):
        results = []
        files = list(self.inbox.glob("*.csv"))
        for path in files:
            try:
                df = self._read_csv(path)
                kind = self.detect_type(df, path.name)

                if kind == "quotes":
                    out = self.normalize_quotes(df)
                    target = self.data_dir / "quotes.csv"
                elif kind == "capital":
                    out = self.normalize_capital(df)
                    target = self.data_dir / "capital.csv"
                elif kind == "portfolio":
                    out = self.normalize_portfolio(df)
                    target = self.data_dir / "portfolio.csv"
                else:
                    results.append({"file": path.name, "status": "skipped", "type": "unknown"})
                    continue

                out.to_csv(target, index=False, encoding="utf-8-sig")
                stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                shutil.move(str(path), str(self.processed / f"{stamp}_{path.name}"))
                results.append({"file": path.name, "status": "imported", "type": kind, "rows": len(out)})

            except Exception as e:
                results.append({"file": path.name, "status": "error", "error": str(e)})

        return results
