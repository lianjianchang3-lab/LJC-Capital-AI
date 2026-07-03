from dataclasses import dataclass


@dataclass
class CapitalSignal:
    code: str
    name: str
    capital_score: float
    capital_health: int
    institution_score: int
    confidence: int
    stage: str
    trend: str
    continuity_stars: str
    net_main: float
    super_large: float
    large: float
    explanation: str
