from engine.engine.research_watch_engine import ResearchWatchEngine
from engine.engine.main_force_engine import MainForceEngine
from engine.engine.scoring_engine import ScoringEngine
from engine.engine.decision_policy_engine import DecisionPolicyEngine
from engine.engine.war_room_engine import WarRoomEngine


class V31DecisionOS:
    """
    LJC Capital AI Pro V3.1 RC 统一入口。
    当前为可运行静态数据版本：先跑通 War Room、长期关注股、主力资金纵向对比、机会池/核心池。
    后续接入真实行情/资金/新闻时，只替换 data_provider。
    """

    def __init__(self):
        self.research = ResearchWatchEngine()
        self.main_force = MainForceEngine()
        self.scoring = ScoringEngine()
        self.policy = DecisionPolicyEngine()
        self.war_room = WarRoomEngine()

    def run_daily(self):
        stocks = self.research.load_watchlist()

        enriched = []
        for stock in stocks:
            mf = self.main_force.evaluate(stock)
            score = self.scoring.score(stock, mf)
            decision = self.policy.decide(stock, mf, score)
            enriched.append({**stock, **mf, **score, **decision})

        enriched = sorted(enriched, key=lambda x: (x["pool_rank"], x["lia"]), reverse=True)

        diamond_core = [s for s in enriched if s["pool"] == "Diamond Core"]
        opportunity = [s for s in enriched if s["pool"] == "Opportunity"]
        priority = [s for s in enriched if s["priority"] in {"S", "A"}]

        war_room = self.war_room.generate(enriched, diamond_core, opportunity)

        return {
            "war_room": war_room,
            "priority_watch": priority[:5],
            "diamond_core": diamond_core[:8],
            "opportunity_pool": opportunity[:10],
            "main_force_summary": [
                f"{s['code']} {s['name']}：1日{s['mf_1d']}，3日{s['mf_3d']}，5日{s['mf_5d']}，趋势：{s['main_force_trend']}，MFS {s['mfs']}"
                for s in enriched[:8]
            ],
            "execution_missions": [
                f"① {war_room['mission']}",
                f"② 做T候选：{war_room['t_candidate']}",
                f"③ 新机会：{war_room['buy_candidate']}",
                "④ 纪律：不追高，低吸优先，做T只用机动仓。",
            ],
            "review_summary": "V3.1 RC 已冻结功能范围：后续只接真实数据、修Bug、优化评分。"
        }
