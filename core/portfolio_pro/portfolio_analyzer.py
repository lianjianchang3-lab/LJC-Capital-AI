import pandas as pd
from core.provider import ProviderManager

class PortfolioProAnalyzer:
    def __init__(self, provider=None):
        self.provider = provider or ProviderManager()

    def analyze(self):
        pf = self.provider.get_portfolio()
        q = self.provider.get_quotes()
        if pf.empty:
            return {"summary": {"status": "NO PORTFOLIO"}, "positions": pd.DataFrame()}
        if "code" in pf.columns and "code" in q.columns:
            price_col = next((c for c in ["price", "最新价", "现价", "close", "实时价"] if c in q.columns), None)
            merged = pf.merge(q[["code", price_col]] if price_col else q[["code"]], on="code", how="left")
        else:
            merged = pf.copy()
        return {"summary": {"status": "OK", "positions": len(merged)}, "positions": merged}
