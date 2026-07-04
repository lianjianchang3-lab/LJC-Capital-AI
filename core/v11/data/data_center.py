from pathlib import Path
from datetime import datetime
import pandas as pd

class DataCenterV11:
    def __init__(self):
        self.csv_sources = [
            ("V10.5缓存", Path("data/realtime/v105_live_cache.csv")),
            ("V101缓存", Path("data/realtime/v101_quotes_cache.csv")),
            ("实时CSV", Path("data/realtime/quotes_realtime.csv")),
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
        df["data_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df

    def quotes(self):
        try:
            from core.v105 import LiveHub105
            df = LiveHub105().quotes()
            if df is not None and not df.empty:
                return self._normalize(df, df["source"].iloc[0] if "source" in df.columns else "V10.5 LiveHub")
        except Exception:
            pass
        for name, path in self.csv_sources:
            if path.exists():
                try:
                    df = self._normalize(pd.read_csv(path), name)
                    if not df.empty:
                        return df
                except Exception:
                    continue
        return pd.DataFrame()

    def health(self):
        df = self.quotes()
        return {"center":"Data Center","version":"V11 RC1","active_source":df["source"].iloc[0] if not df.empty and "source" in df.columns else "等待数据","rows":len(df),"ready":not df.empty,"updated_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    def quality(self):
        df = self.quotes()
        if df.empty:
            return {"score":0,"missing":"no data"}
        required = ["code","name","price","change_pct","amount","risk","lia","capital"]
        missing = [c for c in required if c not in df.columns]
        score = max(0, 100 - len(missing)*10)
        return {"score":score,"missing":missing,"rows":len(df)}
