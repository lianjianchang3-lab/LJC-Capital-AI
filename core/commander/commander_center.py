from datetime import datetime
from core.strategy_v3 import MasterStrategyV3
from core.trading_plan import TradingPlanEngine
from core.alerts import AlertCenter
from core.official import OfficialValidation

class CommanderCenter:
    def snapshot(self):
        strategy = MasterStrategyV3().generate()
        trading = TradingPlanEngine().generate()
        alerts = AlertCenter().scan()
        validation = OfficialValidation().validate()
        market = strategy.get("market", {})
        return {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "market": market,
            "suggested_total_position": trading.get("suggested_total_position"),
            "top_plan_count": len(trading.get("plans", [])),
            "alert_count": alerts.get("alert_count"),
            "official_status": validation.get("overall"),
            "final_decision": self._decision(market, alerts),
            "risk_note": "CSV模式：非实时行情，实盘前必须导入最新数据。",
        }

    def _decision(self, market, alerts):
        regime = market.get("regime")
        alert_count = alerts.get("alert_count", 0)
        if regime == "Risk OFF":
            return "防御优先：控制总仓位，重点观察高评分低风险个股。"
        if alert_count > 5:
            return "机会存在但预警较多：分批操作，严格止损。"
        return "结构性机会：按交易计划执行，避免追高。"
