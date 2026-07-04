from core.v83 import V83ProviderManager, AlphaValidationCenter, LearningEngine, PortfolioAI, InstitutionCommittee

def test_v83_data():
    assert "engine" in V83ProviderManager().health()

def test_v83_alpha_learning_portfolio_committee():
    assert "cards" in AlphaValidationCenter().validate()
    assert "weights" in LearningEngine().calibrate()
    assert "allocations" in PortfolioAI().propose()
    assert "votes" in InstitutionCommittee().meeting()
