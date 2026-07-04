from datetime import datetime
from core.market_intel import MarketIntelligence
from core.signal import SignalEngine

class ReportEngine:
    def daily_brief(self):
        market = MarketIntelligence().snapshot()
        signals = SignalEngine().signals()
        top = []
        if hasattr(signals, "empty") and not signals.empty:
            top = signals.head(5)[["code","name","lia","signal","action"]].to_dict("records")
        return {
            "title": "LJC Daily Brief 2.0",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "market": market,
            "top": top,
            "risk_note": "当前仍为CSV模式，实盘前必须导入最新数据。",
        }
