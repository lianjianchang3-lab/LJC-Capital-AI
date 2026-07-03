from pathlib import Path
from datetime import datetime
import json
import pandas as pd


class CloudBridge:
    def __init__(self, cloud_dir="cloud", data_dir="data"):
        self.cloud_dir = Path(cloud_dir)
        self.data_dir = Path(data_dir)
        self.cloud_dir.mkdir(parents=True, exist_ok=True)
        self.live_file = self.cloud_dir / "live_state.json"

    def _read_csv(self, name):
        path = self.data_dir / name
        if not path.exists():
            return []
        try:
            return pd.read_csv(path, dtype={"code": str}).to_dict(orient="records")
        except Exception:
            return []

    def publish(self, extra=None):
        state = {
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "mac_local_bridge",
            "mode": "semi_cloud_realtime",
            "quotes": self._read_csv("quotes.csv"),
            "capital": self._read_csv("capital.csv"),
            "portfolio": self._read_csv("portfolio.csv"),
            "extra": extra or {},
        }
        self.live_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        return {
            "ok": True,
            "file": str(self.live_file),
            "updated_at": state["updated_at"],
            "quotes": len(state["quotes"]),
            "capital": len(state["capital"]),
        }

    def load(self):
        if not self.live_file.exists():
            return {
                "ok": False,
                "message": "尚未发布云桥数据。",
                "updated_at": None,
                "quotes": [],
                "capital": [],
            }
        try:
            return json.loads(self.live_file.read_text(encoding="utf-8"))
        except Exception as e:
            return {
                "ok": False,
                "message": str(e),
                "updated_at": None,
                "quotes": [],
                "capital": [],
            }

    def status(self):
        data = self.load()
        if not data or data.get("ok") is False:
            return {
                "status": "未同步",
                "updated_at": None,
                "message": data.get("message", "无云端数据") if isinstance(data, dict) else "无云端数据",
            }
        return {
            "status": "已同步",
            "updated_at": data.get("updated_at"),
            "message": "Cloud Bridge 数据可用",
        }
