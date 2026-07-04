from core.provider import ProviderManager
from core.decision import DecisionEngineV2
from core.backtest import BacktestEngine
from core.cloud import CloudSync
from core.report_center import ReportEngine

def test_provider_manager():
    assert "active_provider" in ProviderManager().health()

def test_decision_engine():
    df = DecisionEngineV2().decisions()
    assert hasattr(df, "empty")

def test_skeletons():
    assert BacktestEngine().run()["status"] == "READY"
    assert "status" in CloudSync().status()
    assert "title" in ReportEngine().daily_brief()
