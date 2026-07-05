from core.pro_v20.tradeplan.trade_planner_v2 import TradePlannerV2
from core.pro_v20.alerts.alert_engine_v2 import AlertEngineV2

class CommanderCenterV2:
    def __init__(self):
        self.planner = TradePlannerV2()
        self.alerts = AlertEngineV2()

    def dashboard(self):
        s = self.planner.commander_summary()
        a = self.alerts.scan()
        s["alerts"] = a.head(20).to_dict("records") if a is not None and not a.empty else []
        return s
