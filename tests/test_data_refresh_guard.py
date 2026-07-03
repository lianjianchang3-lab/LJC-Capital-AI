from core.status import DataRefreshGuard


def test_refresh_guard():
    s = DataRefreshGuard().all_status()
    assert "files" in s
    assert "needs_update" in s
