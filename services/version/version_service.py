from pathlib import Path


class VersionService:
    def __init__(self, version_file: str = "VERSION"):
        self.version_file = Path(version_file)

    def current(self):
        if self.version_file.exists():
            return self.version_file.read_text(encoding="utf-8").strip()
        return "8.0.0-alpha.1"

    def build_info(self):
        return {
            "version": self.current(),
            "architecture": "V8.0 Master",
            "status": "alpha",
        }
