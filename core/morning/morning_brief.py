from core.decision import DecisionEngine
from core.lia import LIAEngine


class MorningBrief:
    def __init__(self, decision_engine=None):
        self.decision_engine = decision_engine or DecisionEngine(LIAEngine())

    def generate(self):
        plan = self.decision_engine.make_plan()
        signals = plan.get("signals", [])

        diamond = plan.get("diamond", [])
        opportunity = plan.get("opportunity", [])
        watch = plan.get("watch", [])

        hot_themes = []
        for s in signals:
            if s.sector >= 88:
                hot_themes.append((s.name, s.sector))
        hot_themes = hot_themes[:5]

        return {
            "title": "LJC Morning Brief",
            "market": plan.get("market", "暂无"),
            "position": plan.get("position", "50%"),
            "risk": plan.get("risk", "未知"),
            "summary": plan.get("summary", ""),
            "diamond": diamond,
            "opportunity": opportunity,
            "watch": watch,
            "hot_themes": hot_themes,
        }
