from dataclasses import dataclass
from typing import Optional


@dataclass
class Quote:
    code: str
    name: str
    price: float
    change_pct: float
    turnover: float
    timestamp: str
    provider: str = "csv"
    latency: Optional[float] = None


@dataclass
class Capital:
    code: str
    name: str
    main_inflow: float
    super_large: float
    large: float
    medium: float
    small: float
    timestamp: str
    provider: str = "csv"


@dataclass
class Signal:
    code: str
    name: str
    price: float
    change_pct: float
    lia: float
    capital_score: int
    risk_score: int
    rank: str
    action: str
    reason: str
