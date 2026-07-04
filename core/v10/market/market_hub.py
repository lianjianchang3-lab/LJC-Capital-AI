import pandas as pd
from pathlib import Path
from datetime import datetime

class V10MarketHub:
    """
    V10.0 统一市场数据中心。
    优先使用 V9.3 RealtimeCore；失败使用 CSV。
    """
    def __init__(self):
        self.csv_sources = [
            ("实时CSV", Path("data/realtime/quotes_realtime.csv")),
            ("导入CSV", Path("data/inbox/quotes.csv")),
            ("本地CSV", Path("data/quotes.csv")),
        ]

    def _normalize(self, df, source):
        if df is None or df.empty:
            return pd.DataFrame()
        df = df.copy()
        rename = {"代码":"code","名称":"name","最新价":"price","涨跌幅":"change_pct","成交额":"amount","成交量":"volume","换手率":"turnover"}
        df = df.rename(columns={k:v for k,v in rename.items() if k in df.columns})
        if "code" in df.columns:
            df["code"] = df["code"].astype(str).str.replace(".0","",regex=False).str.zfill(6)
        if "name" not in df.columns:
            df["name"] = df["code"] if "code" in df.columns else ""
        for col in ["price","change_pct","amount","volume","turnover","main_inflow","trend","capital","risk","quality","lia","sector"]:
            if col not in df.columns:
                df[col] = 0 if col != "sector" else "未知"
        for col in ["price","change_pct","amount","volume","turnover","main_inflow","trend","capital","risk","quality","lia"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        df["source"] = source
        df["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df

    def quotes(self):
        try:
            from core.v93 import RealtimeCore
            df = RealtimeCore().quotes()
            if df is not None and not df.empty:
                return self._normalize(df, df["source"].iloc[0] if "source" in df.columns else "V9.3实时核心")
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
        return {
            "engine": "V10.0 Market Hub",
            "active_source": df["source"].iloc[0] if not df.empty and "source" in df.columns else "等待数据",
            "rows": len(df),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ready": not df.empty,
        }
