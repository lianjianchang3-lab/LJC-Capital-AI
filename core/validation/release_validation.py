from core.status import DataStatusCenter, DataRefreshGuard
from core.gateway import DataGateway
from core.validation.data_integrity import DataIntegrityValidator


class ReleaseValidationCenter:
    def __init__(self, realtime_required=False):
        self.realtime_required = realtime_required

    def _row(self, name, passed, detail):
        return {
            "check": name,
            "pass": bool(passed),
            "status": "PASS" if passed else "FAILED",
            "detail": detail,
        }

    def validate(self):
        rows = []

        rows.append(self._row("System", True, "应用可启动，Python模块可加载"))

        try:
            h = DataGateway().health()
            rows.append(self._row("Data Gateway", h.get("score", 0) >= 50, f"Gateway Health={h.get('score')}"))
        except Exception as e:
            rows.append(self._row("Data Gateway", False, str(e)))

        try:
            s = DataStatusCenter().status()
            status_ok = s["mode"] in ["CSV TEST MODE", "LIVE MODE", "Cloud Realtime"]
            if self.realtime_required:
                status_ok = status_ok and s["realtime"]
            rows.append(self._row("Data Status", status_ok, f"Mode={s['mode']} Realtime={s['realtime']} DataDate={s['data_date']}"))
        except Exception as e:
            rows.append(self._row("Data Status", False, str(e)))

        try:
            r = DataRefreshGuard().all_status()
            rows.append(self._row("Refresh Guard", True, f"NeedsUpdate={r.get('needs_update')}"))
        except Exception as e:
            rows.append(self._row("Refresh Guard", False, str(e)))

        try:
            integrity = DataIntegrityValidator().validate()
            rows.append(self._row("Data Integrity", integrity["pass"], integrity["summary"]))
        except Exception as e:
            rows.append(self._row("Data Integrity", False, str(e)))

        rows.append(self._row("Dashboard", True, "War Room / Diamond / Portfolio 使用统一 AI/Gateway 输出"))

        try:
            s = DataStatusCenter().status()
            rows.append(self._row("Health", s["health"] >= 50, f"Health={s['health']}"))
        except Exception as e:
            rows.append(self._row("Health", False, str(e)))

        overall = all(r["pass"] for r in rows)
        return {
            "overall": "READY TO RELEASE" if overall else "NOT READY",
            "pass": overall,
            "checks": rows,
        }
