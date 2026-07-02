from engine_v32.main_force_timeline import MainForceTimelineEngine


class V32DecisionOS:
    def __init__(self):
        self.main_force = MainForceTimelineEngine()
        self.stocks = [
            {"code": "300136", "name": "信维通信", "base": 94, "risk": 18, "theme": "商业航天/AI基础设施"},
            {"code": "300762", "name": "上海瀚讯", "base": 95, "risk": 20, "theme": "商业航天/军工通信"},
            {"code": "603308", "name": "应流股份", "base": 88, "risk": 26, "theme": "商业航天/高端制造"},
            {"code": "688008", "name": "澜起科技", "base": 91, "risk": 22, "theme": "AI基础设施/半导体"},
            {"code": "688387", "name": "信科移动", "base": 86, "risk": 30, "theme": "卫星通信"},
        ]

    def _score(self, stock, mf):
        lia = round(stock["base"] * 0.55 + mf["capital_health"] * 0.35 + (100 - stock["risk"]) * 0.10, 1)
        confidence = round(min(98, lia - stock["risk"] * 0.05), 1)

        if lia >= 90 and mf["capital_health"] >= 88 and stock["risk"] <= 25:
            pool, action, priority = "Diamond Core", "持有/低吸做T", "S"
        elif lia >= 84 and mf["capital_health"] >= 78:
            pool, action, priority = "Opportunity", "等待右侧确认", "A"
        else:
            pool, action, priority = "Watch", "持续跟踪", "B"

        if mf["capital_state"] == "资金转弱":
            action, priority = "降级观察/不加仓", "C"

        return {
            **stock,
            **mf,
            "lia": lia,
            "confidence": confidence,
            "pool": pool,
            "action": action,
            "priority": priority,
            "evidence": f"{mf['capital_state']}，5日主力合计 {mf['mf_5d']} 亿，风险 {stock['risk']}",
        }

    def run(self):
        rows = [self._score(s, self.main_force.analyze(s["code"])) for s in self.stocks]
        rows = sorted(rows, key=lambda x: (x["priority"] == "S", x["lia"]), reverse=True)

        diamond = [r for r in rows if r["pool"] == "Diamond Core"]
        opportunity = [r for r in rows if r["pool"] == "Opportunity"]
        watch = [r for r in rows if r["pool"] == "Watch"]

        buy = opportunity[0]["name"] if opportunity else "暂无"
        t = diamond[0]["name"] if diamond else "暂无"
        avg_conf = round(sum(r["confidence"] for r in rows) / len(rows), 1)

        return {
            "war_room": {
                "market": "机构主线",
                "position": "75%" if avg_conf >= 86 else "60%",
                "theme": "商业航天 / AI基础设施",
                "risk": "LOW",
                "mission": f"重点关注 {buy}；做T候选 {t}；资金转弱股票不加仓。",
                "confidence": avg_conf,
            },
            "diamond": diamond,
            "opportunity": opportunity,
            "watch": watch,
            "alerts": self._alerts(rows),
        }

    def _alerts(self, rows):
        alerts = []
        for r in rows:
            if r["capital_health"] >= 90:
                alerts.append(f"🟢 {r['name']}：主力资金连续增强，Capital Health {r['capital_health']}")
            if r["capital_state"] == "资金转弱":
                alerts.append(f"🔴 {r['name']}：资金转弱，进入降级观察")
        return alerts or ["暂无重大预警"]
