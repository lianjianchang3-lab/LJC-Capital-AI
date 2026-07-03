from core.lia import LIAEngine


class DecisionEngine:
    def __init__(self, lia_engine=None):
        self.lia_engine = lia_engine or LIAEngine()

    def make_plan(self):
        signals = self.lia_engine.analyze_all()
        if not signals:
            return {
                "market": "暂无数据",
                "position": "50%",
                "risk": "未知",
                "diamond": [],
                "opportunity": [],
                "watch": [],
                "summary": "数据不足，暂不生成作战计划。",
            }

        avg_lia = sum(s.lia for s in signals) / len(signals)
        avg_cap = sum(s.capital for s in signals) / len(signals)

        if avg_lia >= 86 and avg_cap >= 80:
            market, position, risk = "Risk ON", "75%-85%", "中低"
        elif avg_lia >= 75:
            market, position, risk = "结构性机会", "55%-70%", "中"
        else:
            market, position, risk = "Risk OFF", "30%-50%", "偏高"

        diamond = [s for s in signals if s.rank == "Diamond"][:3]
        opportunity = [s for s in signals if s.rank == "Opportunity"][:4]
        watch = [s for s in signals if s.rank == "Watch"][:5]

        top = signals[0]
        summary = f"今日重点：{top.name}。策略：{top.action}。市场状态：{market}。"

        return {
            "market": market,
            "position": position,
            "risk": risk,
            "diamond": diamond,
            "opportunity": opportunity,
            "watch": watch,
            "summary": summary,
            "signals": signals,
        }
