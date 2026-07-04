from datetime import datetime
from core.commander import CommanderCenter
from core.institutional.capital_matrix import InstitutionCapitalMatrix
from core.institutional.market_breadth_pro import MarketBreadthPro
from core.institutional.portfolio_ai_v4 import PortfolioAIV4
from core.reports_pro import ReportCenterPro

class InvestmentOS:
    def dashboard(self):
        commander = CommanderCenter().snapshot()
        capital = InstitutionCapitalMatrix().analyze()
        breadth = MarketBreadthPro().snapshot()
        portfolio = PortfolioAIV4().analyze()
        return {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "commander": commander,
            "capital": capital,
            "breadth": breadth,
            "portfolio": portfolio,
            "final": commander.get("final_decision"),
            "warning": "当前为CSV模式，非实时行情。",
        }

    def one_click_report(self):
        return ReportCenterPro().markdown()
