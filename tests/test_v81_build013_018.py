from core.tracker import InstitutionTracker
from core.regime import MarketRegimeEngine
from core.scoring import StockScoringV2
from core.position import PositionManager
from core.rotation import SectorRotation
from core.committee import InvestmentCommittee

def test_phase3_modules():
    assert "status" in InstitutionTracker().track()
    assert "regime" in MarketRegimeEngine().detect()
    assert hasattr(StockScoringV2().score(), "empty")
    assert "status" in PositionManager().advise()
    assert "status" in SectorRotation().analyze()
    assert "final_decision" in InvestmentCommittee().run()
