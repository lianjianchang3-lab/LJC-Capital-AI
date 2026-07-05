from core.enterprise.config_manager import ConfigManager
from core.enterprise.module_registry import ModuleRegistry
from core.enterprise.service_locator import ServiceLocator


class DecisionHub:
    """
    V7 统一决策枢纽。
    先不破坏旧代码，把已有 DecisionCore / AITrader / Institution / Radar 统一挂载。
    """

    def __init__(self):
        self.config = ConfigManager()
        self.registry = ModuleRegistry()
        self.services = ServiceLocator()
        self._bootstrap()

    def _bootstrap(self):
        from core.decision import DecisionCore
        from core.radar import MarketRadar

        self.services.set("decision", DecisionCore())
        self.services.set("radar", MarketRadar())

        try:
            from core.trader import AITrader
            self.services.set("trader", AITrader())
        except Exception:
            pass

        try:
            from core.institution import InstitutionEngine
            self.services.set("institution", InstitutionEngine())
        except Exception:
            pass

    def decision(self):
        return self.services.get("decision")

    def radar(self):
        return self.services.get("radar")

    def market(self):
        return self.decision().market()

    def trade_plan(self):
        return self.decision().trade_plan()

    def portfolio(self):
        return self.decision().portfolio()

    def morning_report(self):
        return self.decision().morning_report()

    def snapshot(self):
        radar = self.radar()
        return {
            "market": self.market(),
            "radar": radar.snapshot() if radar else {},
            "services": self.services.names(),
            "configs": self.config.summary(),
        }
