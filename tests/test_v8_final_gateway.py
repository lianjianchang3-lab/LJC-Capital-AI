from core.gateway import DataGateway
from core.ai import V8FinalAI

def test_gateway_health():
    h = DataGateway().health()
    assert "score" in h

def test_ai_signals():
    signals = V8FinalAI().signals()
    assert isinstance(signals, list)
