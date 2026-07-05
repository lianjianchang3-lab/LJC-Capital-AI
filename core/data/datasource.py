from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd

class DataSource(ABC):
    @abstractmethod
    def quotes(self) -> pd.DataFrame:
        ...

class MultiSourceAdapter(DataSource):
    """
    统一数据源适配器：
    优先复用当前已跑通的 core.multisource.MultiSourceRealtimeHub。
    """
    def quotes(self):
        try:
            from core.multisource import MultiSourceRealtimeHub
            df = MultiSourceRealtimeHub().score()
            if df is not None and not df.empty:
                return self._normalize(df, "MultiSourceRealtimeHub")
        except Exception:
            pass

        for path, name in [
            ("data/realtime/multisource_quotes_cache.csv", "多源缓存"),
            ("data/realtime/monday_quotes_cache.csv", "Monday缓存"),
            ("data/realtime/quotes_realtime.csv", "实时CSV"),
            ("data/quotes.csv", "本地CSV"),
        ]:
            try:
                df = pd.read_csv(path, dtype={"code": str})
                if df is not None and not df.empty:
                    return self._normalize(df, name)
            except Exception:
                continue

        return pd.DataFrame()

    def _normalize(self, df, source):
        df = df.copy()
        rename = {
            "代码": "code",
            "名称": "name",
            "最新价": "price",
            "涨跌幅": "change_pct",
            "成交量": "volume",
            "成交额": "amount",
        }
        df = df.rename(columns={k:v for k,v in rename.items() if k in df.columns})
        if "code" in df.columns:
            df["code"] = df["code"].astype(str).str.replace(".0","",regex=False).str.zfill(6)
        if "name" not in df.columns:
            df["name"] = df["code"] if "code" in df.columns else ""
        for c in ["price","change_pct","volume","amount","risk","LJC实时分","Alpha2.0","资金共振","综合风险"]:
            if c not in df.columns:
                df[c] = 0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
        df["source"] = df.get("source", source)
        df["dataos_source"] = source
        df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df
