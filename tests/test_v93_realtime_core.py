from core.v93 import RealtimeCore, RealtimeHealth

def test_realtime_core_health():
    h = RealtimeCore().health()
    assert "engine" in h
    assert "active_source" in h

def test_realtime_health():
    assert "engine" in RealtimeHealth().check()
