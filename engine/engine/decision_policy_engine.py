class DecisionPolicyEngine:
    """
    统一决策策略。
    所有 BUY / HOLD / T / REDUCE 必须从这里输出。
    """

    def decide(self, stock, mf, score):
        lia = score["lia"]
        mfs = mf["mfs"]
        risk = stock["risk"]

        if lia >= 90 and mfs >= 85 and risk <= 25:
            pool = "Diamond Core"
            action = "持有/低吸做T"
            priority = "S"
            pool_rank = 4
        elif lia >= 84 and mfs >= 78 and risk <= 35:
            pool = "Opportunity"
            action = "升级观察/等待右侧确认"
            priority = "A"
            pool_rank = 3
        elif lia >= 76:
            pool = "Watch"
            action = "持续跟踪"
            priority = "B"
            pool_rank = 2
        else:
            pool = "Archive"
            action = "暂不参与"
            priority = "C"
            pool_rank = 1

        if mf["main_force_trend"] == "转弱":
            action = "降级观察/不加仓"
            priority = "C"

        return {
            "pool": pool,
            "action": action,
            "priority": priority,
            "pool_rank": pool_rank,
            "risk_level": "LOW" if risk <= 25 else ("MEDIUM" if risk <= 40 else "HIGH"),
        }
