from core.lia import LIAEngine
from core.decision import DecisionEngine
from core.portfolio import PortfolioEngine
from updater import UpdateService


def test_lia_engine():
    signals = LIAEngine().analyze_all()
    assert isinstance(signals, list)
    assert len(signals) >= 1
    assert signals[0].lia >= 0


def test_decision_plan():
    plan = DecisionEngine().make_plan()
    assert "market" in plan
    assert "position" in plan


def test_portfolio():
    df = PortfolioEngine().analyze()
    assert "LIA" in df.columns


def test_updater():
    status = UpdateService().check()
    assert status["enabled"] is True
