from dataclasses import dataclass


@dataclass
class LIASignal:
    code: str
    name: str
    lia: float
    capital: int
    trend: int
    sector: int
    risk: int
    confidence: int
    rank: str
    action: str
    explanation: str
