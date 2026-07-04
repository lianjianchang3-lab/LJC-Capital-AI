from core.strategy_v3 import MasterStrategyV3

class TradingPlanEngine:
    def __init__(self):
        self.master = MasterStrategyV3()

    def generate(self):
        s = self.master.generate()
        market = s.get("market", {})
        plans = []
        for p in s.get("top_plans", []):
            plans.append({
                "code": p.get("code"),
                "name": p.get("name"),
                "decision": p.get("decision"),
                "position": p.get("position"),
                "entry": p.get("entry_price"),
                "add": p.get("add_price"),
                "stop": p.get("stop_loss"),
                "target1": p.get("target1"),
                "target2": p.get("target2"),
                "reason": p.get("reason"),
            })
        return {
            "market_regime": market.get("regime"),
            "suggested_total_position": "30%-50%" if market.get("regime") == "Risk OFF" else "50%-80%",
            "plans": plans,
            "note": "本交易计划基于当前CSV数据和评分模型；实盘前必须更新数据并人工确认。",
        }
