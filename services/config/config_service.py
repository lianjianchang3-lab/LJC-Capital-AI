from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None


class ConfigService:
    def __init__(self, path: str = "config/settings.yaml"):
        self.path = Path(path)
        self._data = self._load()

    def _load(self):
        if not self.path.exists():
            return {}
        text = self.path.read_text(encoding="utf-8")
        if yaml:
            return yaml.safe_load(text) or {}
        return {"raw": text}

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def all(self):
        return self._data
