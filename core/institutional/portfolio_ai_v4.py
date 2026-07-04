from core.provider import ProviderManager
from core.strategy_v3 import MasterStrategyV3

class PortfolioAIV4:
    def analyze(self):
        pf = ProviderManager().get_portfolio()
        strategy = MasterStrategyV3().generate()
        plans = strategy.get("top_plans", [])
        if pf.empty:
            return {
                "status": "NO PORTFOLIO",
                "health": 70,
                "risk_budget": "未导入持仓",
                "rebalance": plans[:5],
                "advice": "先使用 Top Plans 建立观察池，再导入持仓做组合优化。",
            }
        return {
            "status": "OK",
            "health": 88,
            "risk_budget": "单股≤20%，总仓位按Commander建议",
            "rebalance": plans[:5],
            "advice": "保留高分低风险，降低低分高风险持仓。",
        }
