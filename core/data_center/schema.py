from dataclasses import dataclass
from typing import Any


@dataclass
class DataQuality:
    source: str
    score: int
    status: str
    message: str = ""


@dataclass
class DataResult:
    data: Any
    quality: DataQuality
