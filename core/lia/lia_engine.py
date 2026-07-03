import pandas as pd
from core.data_center import DataCenter
from core.capital import CapitalEngine
from core.lia.schema import LIASignal


class LIAEngine:
    def __init__(self, data_center=None):
        self.dc = data_center or DataCenter()
        self.capital_engine = CapitalEngine(self.dc)

    def _safe_float(self, value, default=0.0):
        try:
            if pd.isna(value):
                return default
            return float(value)
        except Exception:
            return default

    def _sector_score(self, theme: str) -> int:
        sector = self.dc.get_sector().data
        if sector.empty:
            return 70
        theme = str(theme or "")
        best = 70
        for _, row in sector.iterrows():
            sec = str(row.get("sector", ""))
            if sec and sec in theme:
                best = max(best, int(self._safe_float(row.get("score", 70), 70)))
        return best

    def _trend_score(self, code: str) -> int:
        quotes = self.dc.get_quotes([code]).data
        if quotes.empty:
            return 60
        q = quotes.iloc[-1]
        chg = self._safe_float(q.get("change_pct", 0))
        vr = self._safe_float(q.get("volume_ratio", 1), 1)
        score = 65 + chg * 3 + (vr - 1) * 12
        return int(max(20, min(98, score)))

    def _risk_score(self, risk) -> int:
        r = self._safe_float(risk, 35)
        return int(max(0, min(100, 100 - r)))

    def _rank(self, lia: float) -> str:
        if lia >= 90:
            return "Diamond"
        if lia >= 82:
            return "Opportunity"
        if lia >= 70:
            return "Watch"
        return "Avoid"

    def _action(self, lia: float, capital: int, risk_score: int) -> str:
        if lia >= 90 and capital >= 85:
            return "继续持有 / 回调低吸"
        if lia >= 82:
            return "等待右侧确认 / 小仓试探"
        if lia >= 70:
            return "观察，不追高"
        return "暂不参与"

    def analyze_all(self):
        watch = self.dc.get_watchlist().data
        if watch.empty:
            return []
        signals = []
        for _, row in watch.iterrows():
            signals.append(self.analyze(str(row["code"]).zfill(6)))
        return sorted(signals, key=lambda x: x.lia, reverse=True)

    def analyze(self, code: str) -> LIASignal:
        code = str(code).zfill(6)
        watch = self.dc.get_watchlist().data
        w = None
        name = code
        theme = ""
        base_lia = 80
        risk_raw = 35
        if not watch.empty:
            hit = watch[watch["code"].astype(str).str.zfill(6) == code]
            if not hit.empty:
                w = hit.iloc[0]
                name = str(w.get("name", code))
                theme = str(w.get("theme", ""))
                base_lia = self._safe_float(w.get("base_lia", 80), 80)
                risk_raw = self._safe_float(w.get("risk", 35), 35)

        cap = self.capital_engine.analyze(code)
        capital_score = cap.capital_health
        trend_score = self._trend_score(code)
        sector_score = self._sector_score(theme)
        risk_score = self._risk_score(risk_raw)

        lia = (
            capital_score * 0.40
            + trend_score * 0.25
            + sector_score * 0.15
            + risk_score * 0.10
            + base_lia * 0.10
        )
        lia = round(max(0, min(100, lia)), 1)
        confidence = int(round((cap.confidence * 0.55) + (sector_score * 0.20) + (risk_score * 0.25)))
        rank = self._rank(lia)
        action = self._action(lia, capital_score, risk_score)

        explanation = (
            f"资金{capital_score}，趋势{trend_score}，板块{sector_score}，"
            f"风险安全度{risk_score}。资金阶段：{cap.stage}。"
        )

        return LIASignal(
            code=code,
            name=name,
            lia=lia,
            capital=capital_score,
            trend=trend_score,
            sector=sector_score,
            risk=risk_score,
            confidence=confidence,
            rank=rank,
            action=action,
            explanation=explanation,
        )
