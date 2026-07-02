class ScoringEngine:
    """
    统一评分：LIA / Research Score / Confidence。
    V3.1 RC 先用可运行规则，后续接真实数据权重。
    """

    def score(self, stock, mf):
        research_score = round(stock["base_lcri"] * 0.55 + mf["mfs"] * 0.35 + (100 - stock["risk"]) * 0.10, 1)
        lia = round(research_score * 0.65 + mf["mfs"] * 0.25 + (100 - stock["risk"]) * 0.10, 1)
        confidence = round(min(98, max(50, lia - stock["risk"] * 0.08)), 1)

        evidence = []
        if mf["mfs"] >= 85:
            evidence.append("主力资金强")
        if mf["main_force_trend"] in {"连续增强", "持续流入"}:
            evidence.append("资金纵向趋势好")
        if stock["base_lcri"] >= 90:
            evidence.append("研究评分高")
        if stock["risk"] <= 25:
            evidence.append("风险可控")

        return {
            "research_score": research_score,
            "lia": lia,
            "confidence": confidence,
            "evidence_summary": "、".join(evidence) if evidence else "信号不足，继续观察",
        }
