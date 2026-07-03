from pathlib import Path
from core.data_center import DataCenter
from core.realtime.providers import SinaRealtimeProvider


class RealtimeQuoteService:
    def __init__(self, data_center=None, output="data/quotes.csv"):
        self.dc = data_center or DataCenter()
        self.provider = SinaRealtimeProvider()
        self.output = Path(output)
        self.output.parent.mkdir(parents=True, exist_ok=True)

    def watchlist_codes(self):
        watch = self.dc.get_watchlist().data
        if watch.empty or "code" not in watch.columns:
            return []
        return [str(x).zfill(6) for x in watch["code"].tolist()]

    def update_quotes(self, codes=None):
        codes = codes or self.watchlist_codes()
        if not codes:
            return {"ok": False, "message": "没有自选股代码。", "rows": 0}

        df = self.provider.fetch_quotes(codes)
        if df.empty:
            return {"ok": False, "message": "实时行情返回为空。", "rows": 0}

        df.to_csv(self.output, index=False, encoding="utf-8-sig")
        return {
            "ok": True,
            "message": "实时行情已更新。",
            "rows": len(df),
            "file": str(self.output),
        }
