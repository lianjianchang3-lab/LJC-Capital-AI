from core.provider import ProviderManager
from core.strategy_v3 import MasterStrategyV3

class PortfolioManagerV3:
    def __init__(self):
        self.provider = ProviderManager()
        self.master = MasterStrategyV3()

    def analyze(self):
        pf = self.provider.get_portfolio()
        strategy = self.master.generate()
        if pf.empty:
            return {
                "status": "NO PORTFOLIO",
                "health": 70,
                "advice": "未导入持仓，先使用 WatchList 和 Top Plans。",
                "rebalance": [],
            }
        return {
            "status": "OK",
            "health": 85,
            "position_count": len(pf),
            "advice": "优先匹配 Master Strategy V3 的 Top Plans，降低低评分持仓。",
            "rebalance": strategy.get("top_plans", [])[:5],
        }
