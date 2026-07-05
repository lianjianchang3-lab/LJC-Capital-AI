from core.pro_v20.decision.decision_center import ProDecisionCenter
from core.pro_v20.watchlist.watchlist_center import ProWatchlistCenter
from core.pro_v20.portfolio.portfolio_center import ProPortfolioCenter

class ProMorningReport:
    def __init__(self):
        self.decision = ProDecisionCenter()
        self.watchlist = ProWatchlistCenter()
        self.portfolio = ProPortfolioCenter()

    def build(self):
        brief = self.decision.morning_brief()
        watch = self.watchlist.analyze()
        portfolio = self.portfolio.analyze()
        return {
            "brief": brief,
            "watchlist_rows": int(len(watch)) if watch is not None else 0,
            "portfolio_status": portfolio.get("status"),
            "portfolio_summary": portfolio.get("summary"),
        }

    def text(self):
        r = self.build()
        b = r.get("brief", {})
        return (
            f"今日策略：{b.get('summary','暂无')}\n"
            f"自选股数量：{r.get('watchlist_rows')}\n"
            f"持仓：{r.get('portfolio_summary')}"
        )

# 兼容旧代码：Sprint2_9 里可能导入 MorningReport
MorningReport = ProMorningReport
