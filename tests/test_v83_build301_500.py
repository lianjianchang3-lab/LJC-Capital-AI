from core.v83.score_v4 import AIScoreV4
from core.v83.portfolio_pro import PortfolioManagerPro
from core.v83.committee_v2 import InstitutionCommitteeV2
from core.v83.decision import AutonomousCommander

def test_ai_score_v4():
    df = AIScoreV4().table()
    assert hasattr(df, "empty")

def test_portfolio_committee_commander():
    assert "positions" in PortfolioManagerPro().plan()
    assert "votes" in InstitutionCommitteeV2().vote()
    assert "final_instruction" in AutonomousCommander().daily_plan()
