from core.v91 import V91RealtimeHub, V91AutoScanner, V91SignalCenter

def test_v91_modules():
    assert "engine" in V91RealtimeHub().health()
    assert "status" in V91AutoScanner().scan()
    assert "signals" in V91SignalCenter().generate()
