from datetime import datetime, timedelta


class CacheService:
    def __init__(self):
        self._cache = {}

    def get(self, key):
        item = self._cache.get(key)
        if not item:
            return None
        value, expires_at = item
        if datetime.now() > expires_at:
            self._cache.pop(key, None)
            return None
        return value

    def set(self, key, value, ttl_seconds=60):
        self._cache[key] = (value, datetime.now() + timedelta(seconds=ttl_seconds))
