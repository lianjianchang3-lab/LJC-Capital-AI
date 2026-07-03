import subprocess
from datetime import datetime
from pathlib import Path


class UpdateService:
    def __init__(self, log_path="logs/update.log"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(exist_ok=True)

    def _log(self, msg):
        line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {msg}"
        self.log_path.write_text(self.log_path.read_text(encoding="utf-8") + line + "\n" if self.log_path.exists() else line + "\n", encoding="utf-8")
        return line

    def check(self):
        return {
            "enabled": True,
            "channel": "develop",
            "status": "manual",
            "message": "Build008 OTA框架已安装。自动后台升级将在后续版本启用。",
        }

    def pull(self):
        self._log("manual git pull origin develop")
        result = subprocess.run(["git", "pull", "origin", "develop"], capture_output=True, text=True)
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
