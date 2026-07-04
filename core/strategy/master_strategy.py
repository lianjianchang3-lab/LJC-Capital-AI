from core.market_intel import MarketIntelligence
from core.signal import SignalEngine
from core.portfolio_intel import PortfolioIntelligence

class MasterStrategyEngine:
    def generate(self):
        market = MarketIntelligence().snapshot()
        sig = SignalEngine().signals()
        portfolio = PortfolioIntelligence().analyze()
        if market.get("regime") == "Risk ON":
            position = "70%-85%"
        elif market.get("regime") == "结构性机会":
            position = "50%-70%"
        else:
            position = "30%-50%"
        focus = []
        reduce = []
        if hasattr(sig, "empty") and not sig.empty:
            focus = sig[sig["signal"].isin(["BUY/HOLD","WATCH_BUY"])].head(5).to_dict("records")
            reduce = sig[sig["signal"].isin(["REDUCE","AVOID"])].head(5).to_dict("records")
        return {
            "market": market,
            "suggested_position": position,
            "focus": focus,
            "reduce": reduce,
            "portfolio": portfolio,
            "final_note": "V8.1 Master Strategy：以机构评分、信号、组合风险统一生成策略。",
        }
