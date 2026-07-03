from pathlib import Path
from datetime import datetime


class LogService:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / "ljc.log"

    def _write(self, level: str, message: str):
        line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [{level}] {message}"
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
        print(line)

    def info(self, message: str):
        self._write("INFO", message)

    def warning(self, message: str):
        self._write("WARN", message)

    def error(self, message: str):
        self._write("ERROR", message)
