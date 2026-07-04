from core.provider import ProviderManager
from core.strategy_v3 import MasterStrategyV3
from core.trading_plan import TradingPlanEngine
from core.alerts import AlertCenter
from core.workbench import WorkbenchEngine

class OfficialValidation:
    def validate(self):
        checks = []
        def row(name, ok, detail):
            checks.append({"check": name, "pass": bool(ok), "status": "PASS" if ok else "FAILED", "detail": detail})

        try:
            h = ProviderManager().health()
            row("Provider", h.get("active_provider") is not None, h.get("active_provider"))
        except Exception as e:
            row("Provider", False, str(e))

        try:
            s = MasterStrategyV3().generate()
            row("Master Strategy", "market" in s, "strategy generated")
        except Exception as e:
            row("Master Strategy", False, str(e))

        try:
            p = TradingPlanEngine().generate()
            row("Trading Plan", "plans" in p, f"plans={len(p.get('plans', []))}")
        except Exception as e:
            row("Trading Plan", False, str(e))

        try:
            a = AlertCenter().scan()
            row("Alert Center", "alerts" in a, f"alerts={a.get('alert_count')}")
        except Exception as e:
            row("Alert Center", False, str(e))

        try:
            r = WorkbenchEngine().report_markdown()
            row("Report Export", len(r) > 20, "markdown ready")
        except Exception as e:
            row("Report Export", False, str(e))

        passed = all(c["pass"] for c in checks)
        return {"overall": "V8.1 OFFICIAL READY" if passed else "NOT READY", "pass": passed, "checks": checks}
