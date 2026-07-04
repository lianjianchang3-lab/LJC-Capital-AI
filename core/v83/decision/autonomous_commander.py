from datetime import datetime
from core.v83.data import V83ProviderManager
from core.v83.score_v4 import AIScoreV4
from core.v83.portfolio_pro import PortfolioManagerPro
from core.v83.committee_v2 import InstitutionCommitteeV2

class AutonomousCommander:
    """
    Build421-500: Realtime Decision Engine + Autonomous Commander
    """
    def __init__(self, capital=1000000):
        self.capital = capital

    def daily_plan(self):
        data_health = V83ProviderManager().health()
        score = AIScoreV4().table()
        portfolio = PortfolioManagerPro(self.capital).plan()
        committee = InstitutionCommitteeV2().vote()

        top = []
        if hasattr(score, "empty") and not score.empty:
            top = score.head(10).to_dict("records")

        return {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "V8.3 Build500 Autonomous Candidate",
            "data_health": data_health,
            "top_ai_scores": top,
            "portfolio_plan": portfolio,
            "committee": committee,
            "final_instruction": self._instruction(portfolio, committee),
            "risk_warning": "研究辅助，不构成自动下单；实盘前必须更新实时数据并人工确认。",
        }

    def _instruction(self, portfolio, committee):
        pos = portfolio.get("total_position_weight", 0)
        if pos == 0:
            return "当前无明确高置信买点，保持观察。"
        if pos <= 0.35:
            return "低仓位试探，优先执行高评分且委员会BUY票数高的标的。"
        return "结构性机会，可分批执行，严格止损。"
