from core.commander import CommanderCenter
from core.trading_plan import TradingPlanEngine
from core.risk_pro import RiskCenterPro
from core.capital_intel import CapitalIntelligence

class AICommitteeV2:
    def meeting(self):
        commander = CommanderCenter().snapshot()
        trading = TradingPlanEngine().generate()
        risk = RiskCenterPro().analyze()
        capital = CapitalIntelligence().analyze()
        final_actions = []
        for p in trading.get("plans", [])[:5]:
            final_actions.append({
                "code": p.get("code"),
                "name": p.get("name"),
                "action": p.get("decision"),
                "position": p.get("position"),
                "entry": p.get("entry"),
                "stop": p.get("stop"),
                "reason": p.get("reason"),
            })
        return {
            "market": commander.get("market"),
            "risk": risk,
            "capital": capital,
            "suggested_total_position": commander.get("suggested_total_position"),
            "final_actions": final_actions,
            "committee_conclusion": commander.get("final_decision"),
            "disclaimer": "本系统输出为研究辅助，不构成直接投资指令。",
        }
