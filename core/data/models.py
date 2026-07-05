from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd

@dataclass
class StockSnapshot:
    code: str
    name: str
    price: float
    change_pct: float
    volume: float
    amount: float
    source: str
    timestamp: str

    def to_dict(self):
        return asdict(self)

@dataclass
class MarketSnapshot:
    timestamp: str
    source: str
    stocks: Dict[str, StockSnapshot]
    raw_rows: int

    def to_dataframe(self):
        return pd.DataFrame([s.to_dict() for s in self.stocks.values()])

    def stock(self, code: str):
        return self.stocks.get(str(code).zfill(6))

    def health(self):
        return {
            "timestamp": self.timestamp,
            "source": self.source,
            "raw_rows": self.raw_rows,
            "stocks": len(self.stocks),
        }
