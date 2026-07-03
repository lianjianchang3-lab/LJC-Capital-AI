from core.capital import CapitalEngine


def test_capital_engine_analyze_all():
    engine = CapitalEngine()
    signals = engine.analyze_all()
    assert isinstance(signals, list)
    assert len(signals) >= 1


def test_capital_signal_has_score:
    engine = CapitalEngine()
    signal = engine.analyze("300136")
    assert signal.capital_health >= 0
    assert signal.confidence >= 0
