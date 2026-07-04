from core.v83.score_v4 import AIScoreV4

class InstitutionCommitteeV2:
    """
    Build381-420: 多Agent投票：趋势、资金、量化、风险、组合、宏观。
    """
    def vote(self):
        df = AIScoreV4().table()
        if df.empty:
            return {"status": "NO DATA", "votes": []}

        votes = []
        for _, r in df.iterrows():
            agents = {
                "trend_ai": "BUY" if r["trend"] >= 75 else "HOLD" if r["trend"] >= 65 else "SELL",
                "capital_ai": "BUY" if r["capital"] >= 75 else "HOLD" if r["capital"] >= 60 else "SELL",
                "quant_ai": "BUY" if r["ai_score_v4"] >= 80 else "HOLD" if r["ai_score_v4"] >= 65 else "SELL",
                "risk_ai": "BUY" if r["risk"] <= 55 else "HOLD" if r["risk"] <= 70 else "SELL",
                "lia_ai": "BUY" if r["lia"] >= 75 else "HOLD" if r["lia"] >= 65 else "SELL",
                "macro_ai": "HOLD",
            }
            buy = sum(1 for v in agents.values() if v == "BUY")
            sell = sum(1 for v in agents.values() if v == "SELL")
            if buy >= 4:
                final = "BUY"
            elif sell >= 3:
                final = "SELL/REDUCE"
            else:
                final = "HOLD/WATCH"
            confidence = round(max(buy, sell, 6-buy-sell) / 6, 2)
            votes.append({
                "code": r.get("code"),
                "name": r.get("name"),
                "ai_score_v4": r.get("ai_score_v4"),
                "final": final,
                "confidence": confidence,
                **agents,
                "reason": r.get("explain_v4"),
            })
        return {"status": "OK", "votes": votes}
