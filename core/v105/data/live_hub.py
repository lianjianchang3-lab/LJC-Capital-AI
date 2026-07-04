from pathlib import Path
from datetime import datetime
import pandas as pd

class LiveHub105:
    def __init__(self):
        self.csv_sources = [
            ("实时CSV", Path("data/realtime/quotes_realtime.csv")),
            ("V101缓存", Path("data/realtime/v101_quotes_cache.csv")),
            ("导入CSV", Path("data/inbox/quotes.csv")),
            ("本地CSV", Path("data/quotes.csv")),
        ]

    def _normalize(self, df, source):
        if df is None or df.empty:
            return pd.DataFrame()
        df = df.copy()
        rename = {"代码":"code","名称":"name","最新价":"price","涨跌幅":"change_pct","成交额":"amount","成交量":"volume","换手率":"turnover","总市值":"market_cap"}
        df = df.rename(columns={k:v for k,v in rename.items() if k in df.columns})
        if "code" in df.columns:
            df["code"] = df["code"].astype(str).str.replace(".0","",regex=False).str.zfill(6)
        if "name" not in df.columns:
            df["name"] = df["code"] if "code" in df.columns else ""
        if "sector" not in df.columns:
            df["sector"] = "未知"
        for col in ["price","change_pct","amount","volume","turnover","main_inflow","trend","capital","risk","quality","lia","market_cap"]:
            if col not in df.columns:
                df[col] = 0
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        df["source"] = source
        df["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df

    def _akshare(self):
        try:
            import akshare as ak
            raw = ak.stock_zh_a_spot_em()
            df = self._normalize(raw, "AKShare东方财富实时")
            if not df.empty:
                Path("data/realtime").mkdir(parents=True, exist_ok=True)
                df.to_csv("data/realtime/v105_live_cache.csv", index=False)
            return df
        except Exception:
            return pd.DataFrame()

    def quotes(self):
        live = self._akshare()
        if not live.empty:
            return live
        for name, path in self.csv_sources:
            if path.exists():
                try:
                    df = self._normalize(pd.read_csv(path), name)
                    if not df.empty:
                        return df
                except Exception:
                    pass
        return pd.DataFrame()

    def health(self):
        df = self.quotes()
        return {
            "engine": "V10.5 LiveHub",
            "active_source": df["source"].iloc[0] if not df.empty else "等待数据",
            "rows": len(df),
            "live_ready": not df.empty and "AKShare" in str(df["source"].iloc[0]),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
