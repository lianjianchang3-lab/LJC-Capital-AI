from core.monday_realtime import MondayRealtimeSystem

def test_monday_realtime_health():
    h = MondayRealtimeSystem().health()
    assert "system" in h
    assert "active_source" in h

def test_monday_realtime_score():
    df = MondayRealtimeSystem().score()
    assert hasattr(df, "empty")
