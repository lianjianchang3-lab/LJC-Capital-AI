from datetime import datetime

class CacheProvider:
    def __init__(self):
        self.cache = {}

    def set(self, key, value):
        self.cache[key] = {"value": value, "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    def get(self, key):
        return self.cache.get(key, {}).get("value")

    def status(self):
        return {"keys": list(self.cache.keys()), "size": len(self.cache)}
