from datetime import datetime
import pandas as pd
from core.provider import ProviderManager

class V83ProviderManager:
    """
    M1 Realtime Data Engine.
    当前使用现有 ProviderManager + CSV fallback。
    未来可在这里接 AkShare / Tushare / EastMoney / Broker。
    """
    def __init__(self, preferred="csv"):
        self.preferred = preferred
        self.base = ProviderManager(mode=preferred if preferred in ["csv","realtime"] else "csv")

    def get_quotes(self):
        df = self.base.get_quotes()
        return self._normalize(df)

    def get_capital(self):
        df = self.base.get_capital()
        return self._normalize(df)

    def get_portfolio(self):
        df = self.base.get_portfolio()
        return self._normalize(df)

    def _normalize(self, df):
        if df is None or df.empty:
            return pd.DataFrame()
        df = df.copy()
        if "code" in df.columns:
            df["code"] = df["code"].astype(str).str.replace(".0","",regex=False).str.zfill(6)
        return df

    def health(self):
        h = self.base.health()
        return {
            "engine": "V8.3 Realtime Data Engine",
            "preferred": self.preferred,
            "active_provider": h.get("active_provider"),
            "mode": h.get("mode"),
            "quotes_rows": len(self.get_quotes()),
            "capital_rows": len(self.get_capital()),
            "portfolio_rows": len(self.get_portfolio()),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fallback": "CSV fallback active until live provider configured",
        }
