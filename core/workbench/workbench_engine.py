from datetime import datetime
from core.strategy_v3 import MasterStrategyV3
from core.selection import SelectionCenter
from core.portfolio_v3 import PortfolioManagerV3

class WorkbenchEngine:
    def __init__(self):
        self.master = MasterStrategyV3()
        self.selection = SelectionCenter()
        self.portfolio = PortfolioManagerV3()

    def daily_plan(self):
        return {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "strategy": self.master.generate(),
            "selection": self.selection.scan(),
            "portfolio": self.portfolio.analyze(),
        }

    def report_markdown(self):
        p = self.daily_plan()
        market = p["strategy"]["market"]
        lines = [
            "# LJC V8.1 AI Daily Workbench",
            f"- Time: {p['time']}",
            f"- Market: {market.get('regime')}",
            f"- Avg LIA: {market.get('avg_lia')}",
            "## Top Plans",
        ]
        for item in p["strategy"].get("top_plans", [])[:5]:
            lines.append(f"- {item.get('code')} {item.get('name')}: {item.get('decision')} / {item.get('position')} / Score {item.get('investment_score')}")
        return "\n".join(lines)
