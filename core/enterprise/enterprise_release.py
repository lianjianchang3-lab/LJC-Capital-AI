from core.official import OfficialValidation
from core.enterprise.enterprise_dashboard import EnterpriseDashboard
from core.risk_pro import RiskCenterPro
from core.capital_intel import CapitalIntelligence
from core.committee_v2 import AICommitteeV2

class EnterpriseRelease:
    def validate(self):
        checks = []
        def add(name, ok, detail):
            checks.append({"check": name, "pass": bool(ok), "status": "PASS" if ok else "FAILED", "detail": detail})
        try:
            add("Official Validation", OfficialValidation().validate().get("pass"), "Official checks")
            add("Enterprise Dashboard", "market" in EnterpriseDashboard().snapshot(), "Dashboard ready")
            add("Risk Center Pro", "risk_level" in RiskCenterPro().analyze(), "Risk ready")
            add("Capital Intelligence", "capital_regime" in CapitalIntelligence().analyze(), "Capital ready")
            add("AI Committee V2", "final_actions" in AICommitteeV2().meeting(), "Committee ready")
        except Exception as e:
            add("Enterprise Exception", False, str(e))
        passed = all(x["pass"] for x in checks)
        return {"overall": "V8.1 ENTERPRISE READY" if passed else "NOT READY", "pass": passed, "checks": checks}
