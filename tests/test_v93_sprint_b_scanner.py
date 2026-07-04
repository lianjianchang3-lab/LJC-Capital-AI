from core.v93 import V93MarketScanner, V93AIScoreV3, V93SignalEngine

def test_v93_scanner_signal():
    assert "status" in V93MarketScanner().scan(top_n=5)
    assert V93AIScoreV3().table(top_n=5) is not None
    assert "signals" in V93SignalEngine().generate()
