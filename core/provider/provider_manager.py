from core.provider.csv_provider import CSVProvider
from core.provider.realtime_provider import RealtimeProvider
from core.provider.cache_provider import CacheProvider

class ProviderManager:
    def __init__(self, mode="csv"):
        self.mode = mode
        self.csv = CSVProvider()
        self.realtime = RealtimeProvider(enabled=False)
        self.cache = CacheProvider()

    def active_provider(self):
        if self.mode == "realtime" and self.realtime.health().get("ready"):
            return self.realtime
        return self.csv

    def get_quotes(self):
        df = self.active_provider().get_quotes()
        self.cache.set("quotes", df)
        return df

    def get_capital(self):
        df = self.active_provider().get_capital()
        self.cache.set("capital", df)
        return df

    def get_portfolio(self):
        df = self.csv.get_portfolio()
        self.cache.set("portfolio", df)
        return df

    def health(self):
        active = self.active_provider()
        return {"active_provider": active.name, "mode": active.mode, "providers": [self.csv.health(), self.realtime.health()], "cache": self.cache.status()}
