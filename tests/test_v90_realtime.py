from core.v90 import V90RealtimeManager, V90DecisionEngine

def test_v90_realtime_manager():
    assert "engine" in V90RealtimeManager().health()

def test_v90_decision_engine():
    assert "version" in V90DecisionEngine().dashboard()
    assert "actions" in V90DecisionEngine().trading_plan()
