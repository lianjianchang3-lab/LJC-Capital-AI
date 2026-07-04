from core.v83 import V83ProviderManager, AlphaValidationCenter, LearningEngine, PortfolioAI, InstitutionCommittee

def test_v83_final_acceptance_modules():
    assert "engine" in V83ProviderManager().health()
    assert "cards" in AlphaValidationCenter().validate()
    assert "weights" in LearningEngine().calibrate()
    assert "allocations" in PortfolioAI().propose()
    assert "votes" in InstitutionCommittee().meeting()
