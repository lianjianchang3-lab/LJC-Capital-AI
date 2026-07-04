from core.enterprise import EnterpriseDashboard, EnterpriseRelease
from core.risk_pro import RiskCenterPro
from core.capital_intel import CapitalIntelligence
from core.committee_v2 import AICommitteeV2

def test_enterprise_modules():
    assert "edition" in EnterpriseDashboard().snapshot()
    assert "risk_level" in RiskCenterPro().analyze()
    assert "capital_regime" in CapitalIntelligence().analyze()
    assert "final_actions" in AICommitteeV2().meeting()
    assert "overall" in EnterpriseRelease().validate()
