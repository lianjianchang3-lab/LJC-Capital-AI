from core.pro_v40.engine.unified_ai_engine import UnifiedAIEngine
from core.pro_v40.signals.institution_signal_center import InstitutionSignalCenter
from core.pro_v40.position.position_controller import PositionController
from core.pro_v40.learning.learning_center import LearningCenter

class V40Commander:
    def __init__(self):
        self.engine = UnifiedAIEngine()
        self.signals = InstitutionSignalCenter()
        self.position = PositionController()
        self.learning = LearningCenter()

    def dashboard(self):
        state = self.engine.market_state()
        sig = self.signals.signals()
        alloc = self.position.allocation()
        learn = self.learning.stats()
        return {
            "state": state,
            "signals": sig.head(10).to_dict("records") if sig is not None and not sig.empty else [],
            "allocation": alloc,
            "learning": learn,
        }
