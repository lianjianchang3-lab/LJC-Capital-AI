class WarRoomEngine:
    """
    War Room 最终首页。
    只输出行动，不输出冗余分析。
    """

    def generate(self, enriched, diamond_core, opportunity):
        buy = opportunity[0]["name"] if opportunity else "暂无"
        t = diamond_core[0]["name"] if diamond_core else "暂无"

        avg_conf = round(sum(s["confidence"] for s in enriched) / max(len(enriched), 1), 1)
        position = "75%" if avg_conf >= 86 else ("60%" if avg_conf >= 78 else "40%")

        return {
            "market_state": "机构主线",
            "position": position,
            "theme": "商业航天 / AI基础设施",
            "risk": "LOW" if avg_conf >= 82 else "MEDIUM",
            "buy_candidate": buy,
            "t_candidate": t,
            "mission": f"Priority：关注{buy}，做T候选{t}，仓位{position}，不追高。",
        }
