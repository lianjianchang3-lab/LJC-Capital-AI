from core.institutional import InstitutionCapitalMatrix, MarketBreadthPro, PortfolioAIV4, InvestmentOS
from core.quant import QuantEngine
from core.macro import MacroAllocationEngine
from core.reports_pro import ReportCenterPro

def test_institutional_modules():
    assert "matrix" in InstitutionCapitalMatrix().analyze()
    assert "status" in MarketBreadthPro().snapshot()
    assert "status" in PortfolioAIV4().analyze()
    assert "commander" in InvestmentOS().dashboard()
    assert hasattr(QuantEngine().factors(), "empty")
    assert "equity" in MacroAllocationEngine().allocate()
    assert "Institutional Report" in ReportCenterPro().markdown()
