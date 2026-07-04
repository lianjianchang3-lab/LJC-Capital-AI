from core.regime import MarketRegimeEngine
from core.position import PositionManager
from core.rotation import SectorRotation
from core.scoring import StockScoringV2

class InvestmentCommittee:
    def run(self):
        regime = MarketRegimeEngine().detect()
        positions = PositionManager().advise()
        rotation = SectorRotation().analyze()
        scores = StockScoringV2().score()
        buy, watch, reduce = [], [], []
        if hasattr(scores, "empty") and not scores.empty:
            buy = scores[(scores["score2"] >= 80) & (scores["risk"] <= 65)].head(5).to_dict("records")
            watch = scores[(scores["score2"] >= 70) & (scores["score2"] < 80)].head(5).to_dict("records")
            reduce = scores[(scores["score2"] < 60) | (scores["risk"] >= 75)].head(5).to_dict("records")
        return {
            "market_regime": regime,
            "suggested_total_position": regime.get("suggested_position"),
            "sector_rotation": rotation,
            "buy_or_hold": buy,
            "watch": watch,
            "reduce_or_avoid": reduce,
            "position_plan": positions,
            "risk_note": "当前仍为CSV模式，实盘前必须导入今日最新CSV或接入实时数据源。",
            "final_decision": "按市场状态控制总仓位，优先保留高score2、低risk、资金强的标的。",
        }
