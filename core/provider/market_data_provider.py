from pathlib import Path
import pandas as pd


class MarketDataProvider:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)

    def _read(self, filename):
        path = self.data_dir / filename
        if not path.exists():
            return pd.DataFrame()
        for enc in ["utf-8-sig", "utf-8", "gbk", "gb18030"]:
            try:
                return pd.read_csv(path, encoding=enc, dtype={"code": str, "代码": str, "证券代码": str})
            except Exception:
                continue
        return pd.DataFrame()

    def _normalize_code_col(self, df):
        if df.empty:
            return df
        df = df.copy()
        if "code" not in df.columns:
            for c in ["代码", "证券代码", "股票代码"]:
                if c in df.columns:
                    df["code"] = df[c]
                    break
        if "code" in df.columns:
            df["code"] = df["code"].astype(str).str.replace(".0", "", regex=False).str.zfill(6)
        return df

    def quotes(self):
        return self._normalize_code_col(self._read("quotes.csv"))

    def capital(self):
        return self._normalize_code_col(self._read("capital.csv"))

    def portfolio(self):
        return self._normalize_code_col(self._read("portfolio.csv"))

    def all(self):
        return {
            "quotes": self.quotes(),
            "capital": self.capital(),
            "portfolio": self.portfolio(),
        }
