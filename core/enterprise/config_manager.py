from pathlib import Path
import json

try:
    import yaml
except Exception:
    yaml = None


class ConfigManager:
    """统一配置入口，兼容 settings.yaml / models.yaml / app.yaml / build015_config.json。"""

    def __init__(self, config_dir="config"):
        self.config_dir = Path(config_dir)
        self._cache = {}

    def load(self, name, default=None):
        if name in self._cache:
            return self._cache[name]

        path = self.config_dir / name
        if not path.exists():
            self._cache[name] = default if default is not None else {}
            return self._cache[name]

        try:
            if path.suffix.lower() in [".yaml", ".yml"] and yaml:
                data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            elif path.suffix.lower() == ".json":
                data = json.loads(path.read_text(encoding="utf-8"))
            else:
                data = path.read_text(encoding="utf-8")
        except Exception as e:
            data = {"_error": str(e), "_file": str(path)}

        self._cache[name] = data
        return data

    def settings(self):
        return self.load("settings.yaml", {})

    def models(self):
        return self.load("models.yaml", {})

    def app(self):
        return self.load("app.yaml", {})

    def build(self):
        return self.load("build015_config.json", {})

    def summary(self):
        return {
            "settings": bool(self.settings()),
            "models": bool(self.models()),
            "app": bool(self.app()),
            "build": bool(self.build()),
        }
