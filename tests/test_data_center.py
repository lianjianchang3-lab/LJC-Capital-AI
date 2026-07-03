from core.data_center import DataCenter


def test_data_center_health():
    dc = DataCenter()
    health = dc.health_check()
    assert "overall_score" in health
    assert "checks" in health


def test_get_quotes():
    dc = DataCenter()
    result = dc.get_quotes()
    assert hasattr(result, "data")
    assert hasattr(result, "quality")
