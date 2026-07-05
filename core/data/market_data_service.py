from datetime import datetime
from core.data.cache import TTLCache, CSVCache
from core.data.datasource import MultiSourceAdapter
from core.data.models import StockSnapshot, MarketSnapshot

class MarketDataService:
    def __init__(self, datasource=None, ttl=5):
        self.datasource = datasource or MultiSourceAdapter()
        self.cache = TTLCache(ttl=ttl)
        self.csv_cache = CSVCache()

    def dataframe(self, use_cache=True):
        if use_cache:
            cached = self.cache.get("market_df")
            if cached is not None:
                return cached
        df = self.datasource.quotes()
        if df is None or df.empty:
            df = self.csv_cache.load()
        else:
            self.csv_cache.save(df)
        self.cache.set("market_df", df)
        return df

    def snapshot(self):
        cached = self.cache.get("market_snapshot")
        if cached is not None:
            return cached

        df = self.dataframe()
        stocks = {}
        source = "NO DATA"
        if df is not None and not df.empty:
            source = str(df["source"].iloc[0]) if "source" in df.columns else str(df.get("dataos_source","unknown"))
            for _, r in df.iterrows():
                code = str(r.get("code","")).zfill(6)
                if not code:
                    continue
                stocks[code] = StockSnapshot(
                    code=code,
                    name=str(r.get("name","")),
                    price=float(r.get("price",0) or 0),
                    change_pct=float(r.get("change_pct",0) or 0),
                    volume=float(r.get("volume",0) or 0),
                    amount=float(r.get("amount",0) or 0),
                    source=str(r.get("source", source)),
                    timestamp=str(r.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
                )
        snap = MarketSnapshot(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            source=source,
            stocks=stocks,
            raw_rows=0 if df is None else len(df),
        )
        self.cache.set("market_snapshot", snap)
        return snap

    def stock(self, code):
        return self.snapshot().stock(code)

    def health(self):
        snap = self.snapshot()
        return snap.health()
