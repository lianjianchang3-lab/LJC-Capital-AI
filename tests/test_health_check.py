from core.health import HealthCheck


def test_health_check():
    result = HealthCheck().run()
    assert "score" in result
    assert "results" in result
