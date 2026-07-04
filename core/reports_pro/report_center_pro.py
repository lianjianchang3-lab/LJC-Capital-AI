from datetime import datetime
from core.commander import CommanderCenter
from core.institutional.capital_matrix import InstitutionCapitalMatrix
from core.institutional.market_breadth_pro import MarketBreadthPro
from core.macro import MacroAllocationEngine

class ReportCenterPro:
    def markdown(self):
        commander = CommanderCenter().snapshot()
        capital = InstitutionCapitalMatrix().analyze()
        breadth = MarketBreadthPro().snapshot()
        macro = MacroAllocationEngine().allocate()
        lines = [
            "# LJC V8.1 Institutional Report",
            f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- Market: {commander.get('market', {}).get('regime')}",
            f"- Position: {commander.get('suggested_total_position')}",
            f"- Breadth: {breadth.get('breadth_pct')}%",
            f"- Emotion: {breadth.get('emotion_cycle')}",
            f"- Institution Score Avg: {capital.get('avg_institution_score')}",
            f"- Macro Allocation: Equity {macro.get('equity')} / Cash {macro.get('cash')}",
            "",
            "## Final Decision",
            commander.get("final_decision", ""),
            "",
            "> CSV模式：非实时行情，实盘前必须导入最新数据。",
        ]
        return "\n".join(lines)
