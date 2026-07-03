from core.realtime.providers import SinaRealtimeProvider


def test_market_code():
    p = SinaRealtimeProvider()
    assert p._market_code("300136") == "sz300136"
    assert p._market_code("688008") == "sh688008"
