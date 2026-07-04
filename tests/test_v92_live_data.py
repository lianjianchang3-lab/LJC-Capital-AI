from core.v92 import V92LiveDataEngine, V92RefreshCenter, V92LiveMonitor

def test_v92_live_engine():
    assert "engine" in V92LiveDataEngine().health()

def test_v92_refresh_monitor():
    assert "status" in V92RefreshCenter().refresh_to_csv()
    assert "status" in V92LiveMonitor().scan()
