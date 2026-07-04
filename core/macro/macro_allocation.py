from core.institutional import MarketBreadthPro

class MacroAllocationEngine:
    def allocate(self):
        b = MarketBreadthPro().snapshot()
        emotion = b.get("emotion_cycle", "防御/冰点")
        if "启动" in emotion:
            return {"risk_appetite": "积极", "equity": "70%", "cash": "30%", "focus": ["商业航天", "AI基础设施", "高端制造"]}
        if "结构性" in emotion:
            return {"risk_appetite": "中性", "equity": "50%", "cash": "50%", "focus": ["核心主线", "高LIA标的"]}
        return {"risk_appetite": "防御", "equity": "30%", "cash": "70%", "focus": ["现金", "低风险观察池"]}
