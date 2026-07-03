from core.cloud_realtime import CloudRealtimeService


def test_cloud_realtime_codes():
    svc = CloudRealtimeService()
    codes = svc.watchlist_codes()
    assert isinstance(codes, list)
