from core.intelligence import InstitutionIntelligenceCore
from core.signal import SignalEngine
from core.market_intel import MarketIntelligence
from core.strategy import MasterStrategyEngine

def test_institution_core():
    df = InstitutionIntelligenceCore().score()
    assert hasattr(df, "empty")

def test_signal_engine():
    df = SignalEngine().signals()
    assert hasattr(df, "empty")

def test_market_and_strategy():
    assert "status" in MarketIntelligence().snapshot()
    assert "suggested_position" in MasterStrategyEngine().generate()
