from core.status import DataStatusCenter


def test_data_status_center():
    s = DataStatusCenter().status()
    assert "mode" in s
    assert "realtime" in s
    assert "health" in s
