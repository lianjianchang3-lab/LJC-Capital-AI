from core.provider import ProviderManager
from core.signal import SignalEngine

class PortfolioIntelligence:
    def __init__(self, provider=None):
        self.provider = provider or ProviderManager()
        self.signal_engine = SignalEngine()

    def analyze(self):
        pf = self.provider.get_portfolio()
        sig = self.signal_engine.signals()
        if pf.empty:
            return {"status": "NO PORTFOLIO", "summary": "暂无持仓CSV", "suggestion": "先导入持仓数据", "positions": []}
        count = len(pf)
        risk_names = []
        if not sig.empty and "signal" in sig.columns and "code" in pf.columns:
            m = pf.merge(sig[["code","signal","lia","risk","action"]], on="code", how="left")
            risk_names = m[m["signal"].isin(["REDUCE","AVOID"])]["code"].astype(str).tolist()
        return {
            "status": "OK",
            "summary": f"持仓数 {count}，风险持仓 {len(risk_names)}",
            "suggestion": "控制单一标的集中度，优先保留高LIA低风险标的",
            "risk_positions": risk_names,
        }
