import pandas as pd
from core.v93.scanner import V93MarketScanner

class V93AIScoreV3:
    def table(self, top_n=100):
        result = V93MarketScanner().scan(top_n=top_n)
        return pd.DataFrame(result.get("items", []))
