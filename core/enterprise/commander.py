from core.enterprise.decision_hub import DecisionHub


class EnterpriseCommander:
    """新统一 Commander：电脑端、手机端、晨报后续都应调用这里。"""

    def __init__(self):
        self.hub = DecisionHub()

    def snapshot(self):
        data = self.hub.snapshot()
        market = data.get("market", {})
        radar = data.get("radar", {})
        health = radar.get("health", {})
        return {
            "market": market,
            "radar_health": health,
            "summary": health.get("summary") or market.get("summary"),
            "lcri_top": radar.get("lcri_top", []),
            "trader_top": radar.get("trader_top", []),
            "institution_top": radar.get("institution_top", []),
            "risk_top": radar.get("risk_top", []),
            "services": data.get("services", []),
            "configs": data.get("configs", {}),
        }
