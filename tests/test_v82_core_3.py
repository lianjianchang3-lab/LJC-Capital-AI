from core.realtime import RealtimeProviderManager
from core.calibration import ModelCalibrator
from core.backtest_v2 import SignalBacktester

def test_realtime_provider():
    assert "status" in RealtimeProviderManager().snapshot()

def test_calibration_and_backtest():
    assert "status" in ModelCalibrator().run()
    assert "status" in SignalBacktester().run()
