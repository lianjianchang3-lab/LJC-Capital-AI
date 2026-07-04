from core.v10 import V10MarketHub, V10FundMonitor, V10SectorRotation, V10AICommittee, V10TradingPlan

def test_v10_modules():
    assert "engine" in V10MarketHub().health()
    assert "status" in V10FundMonitor().analyze()
    assert "status" in V10SectorRotation().rank()
    assert "status" in V10AICommittee().decide()
    assert "plans" in V10TradingPlan().generate()
