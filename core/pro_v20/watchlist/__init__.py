try:
    from core.pro_v20.watchlist.watchlist_center import ProWatchlistCenter
except Exception:
    ProWatchlistCenter = None

__all__ = ["ProWatchlistCenter"]
