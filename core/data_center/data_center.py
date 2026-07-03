from plugins.csv_provider.csv_provider import CSVProvider


class DataCenter:
    """
    V8 Build002 Data Center MVP.

    所有后续引擎必须通过 DataCenter 获取数据：
    - get_watchlist
    - get_quotes
    - get_capital
    - get_sector
    - get_news
    """

    def __init__(self, provider=None):
        self.provider = provider or CSVProvider()

    def get_watchlist(self):
        return self.provider.fetch_watchlist()

    def get_quotes(self, symbols=None):
        return self.provider.fetch_quotes(symbols)

    def get_capital(self, symbols=None):
        return self.provider.fetch_capital(symbols)

    def get_sector(self):
        return self.provider.fetch_sector()

    def get_news(self, symbols=None):
        return self.provider.fetch_news(symbols)

    def health_check(self):
        checks = {
            "watchlist": self.get_watchlist().quality,
            "quotes": self.get_quotes().quality,
            "capital": self.get_capital().quality,
            "sector": self.get_sector().quality,
            "news": self.get_news().quality,
        }
        overall = min(q.score for q in checks.values()) if checks else 0
        return {
            "overall_score": overall,
            "checks": checks,
        }
