import math
import pandas as pd

from core.data_center import DataCenter
from core.capital.schema import CapitalSignal


class CapitalEngine:
    """
    V8 Build003 Capital Engine.

    输入：DataCenter 中的统一 capital.csv / quotes.csv
    输出：CapitalSignal
    """

    def __init__(self, data_center=None):
        self.dc = data_center or DataCenter()

    def _safe_float(self, value, default=0.0):
        try:
            if pd.isna(value):
                return default
            return float(value)
        except Exception:
            return default

    def _stage(self, score: float) -> str:
        if score >= 90:
            return "持续吸筹"
        if score >= 75:
            return "温和吸筹"
        if score >= 55:
            return "分歧整理"
        if score >= 35:
            return "高位派发"
        return "快速出货"

    def _stars(self, score: float) -> str:
        if score >= 90:
            return "★★★★★"
        if score >= 75:
            return "★★★★☆"
        if score >= 60:
            return "★★★☆☆"
        if score >= 40:
            return "★★☆☆☆"
        return "★☆☆☆☆"

    def _trend_symbol(self, net_main: float) -> str:
        if net_main >= 2:
            return "↑↑↑"
        if net_main > 0:
            return "↑↑"
        if net_main == 0:
            return "→"
        if net_main > -2:
            return "↓↓"
        return "↓↓↓"

    def analyze_all(self):
        watch = self.dc.get_watchlist().data
        if watch.empty:
            return []
        return [self.analyze(str(row["code"]).zfill(6)) for _, row in watch.iterrows()]

    def analyze(self, code: str) -> CapitalSignal:
        code = str(code).zfill(6)
        capital = self.dc.get_capital([code]).data
        quotes = self.dc.get_quotes([code]).data
        watch = self.dc.get_watchlist().data

        name = code
        if not watch.empty and "code" in watch.columns:
            hit = watch[watch["code"].astype(str).str.zfill(6) == code]
            if not hit.empty:
                name = str(hit.iloc[0].get("name", code))

        if capital.empty:
            return CapitalSignal(
                code=code,
                name=name,
                capital_score=0,
                capital_health=0,
                institution_score=0,
                confidence=0,
                stage="暂无资金数据",
                trend="→",
                continuity_stars="★☆☆☆☆",
                net_main=0,
                super_large=0,
                large=0,
                explanation="没有找到资金数据。",
            )

        row = capital.iloc[-1]
        super_large = self._safe_float(row.get("super_large", 0))
        large = self._safe_float(row.get("large", 0))
        medium = self._safe_float(row.get("medium", 0))
        small = self._safe_float(row.get("small", 0))
        net_main = self._safe_float(row.get("net_main", super_large + large))

        turnover = 0.0
        change_pct = 0.0
        volume_ratio = 1.0
        if not quotes.empty:
            q = quotes.iloc[-1]
            turnover = self._safe_float(q.get("turnover", 0))
            change_pct = self._safe_float(q.get("change_pct", 0))
            volume_ratio = self._safe_float(q.get("volume_ratio", 1), 1)

        main_intensity = 50
        if turnover > 0:
            main_intensity = max(0, min(100, 50 + (net_main / max(turnover, 1)) * 500))

        super_score = max(0, min(100, 50 + super_large * 18))
        large_score = max(0, min(100, 50 + large * 14))
        volume_score = max(0, min(100, 50 + (volume_ratio - 1) * 30))
        price_bonus = 8 if change_pct > 1 else (-8 if change_pct < -2 else 0)

        raw_score = (
            main_intensity * 0.40
            + super_score * 0.25
            + large_score * 0.20
            + volume_score * 0.10
            + (50 + price_bonus) * 0.05
        )

        capital_score = round(max(0, min(100, raw_score)), 1)
        capital_health = int(round(capital_score))
        institution_score = int(round(max(0, min(100, capital_score + super_large * 2 + large))))
        confidence = int(round(max(40, min(98, 65 + abs(net_main) * 8 + min(volume_ratio, 3) * 6))))

        stage = self._stage(capital_score)
        stars = self._stars(capital_score)
        trend = self._trend_symbol(net_main)

        if net_main > 0 and capital_score >= 75:
            explanation = f"主力净流入{net_main:.2f}亿，超大单与大单偏强，资金阶段为{stage}。"
        elif net_main > 0:
            explanation = f"主力小幅净流入{net_main:.2f}亿，资金处于{stage}。"
        elif net_main < 0:
            explanation = f"主力净流出{abs(net_main):.2f}亿，资金阶段为{stage}，需要控制风险。"
        else:
            explanation = "主力资金变化不明显，暂以观察为主。"

        return CapitalSignal(
            code=code,
            name=name,
            capital_score=capital_score,
            capital_health=capital_health,
            institution_score=institution_score,
            confidence=confidence,
            stage=stage,
            trend=trend,
            continuity_stars=stars,
            net_main=round(net_main, 2),
            super_large=round(super_large, 2),
            large=round(large, 2),
            explanation=explanation,
        )
