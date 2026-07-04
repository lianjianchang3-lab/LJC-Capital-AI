from core.market_intel import MarketIntelligence
from core.strategy_v3.score_v3 import ScoreV3
from core.strategy_v3.entry_exit_engine import EntryExitEngine
from core.strategy_v3.position_ai import PositionAI

class MasterStrategyV3:
    def __init__(self):
        self.market = MarketIntelligence()
        self.score = ScoreV3()
        self.entry_exit = EntryExitEngine()
        self.position_ai = PositionAI()

    def generate(self):
        market = self.market.snapshot()
        plans = self.entry_exit.plans()
        top = []
        for p in plans[:10]:
            p = dict(p)
            p["position"] = self.position_ai.suggest(market.get("regime"), p.get("investment_score", 0), p.get("risk", 50))
            top.append(p)
        return {
            "market": market,
            "top_plans": top,
            "summary": f"市场={market.get('regime')}，优先处理评分最高且风险可控的股票。",
            "warning": "当前仍基于CSV数据，实盘前必须导入最新数据。",
        }
