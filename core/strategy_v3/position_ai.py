class PositionAI:
    def suggest(self, market_regime, score, risk):
        if market_regime == "Risk ON" and score >= 85 and risk < 65:
            return "重仓候选 15%-20%"
        if score >= 78 and risk < 70:
            return "标准仓位 8%-12%"
        if score >= 70:
            return "观察仓位 3%-5%"
        if risk >= 75:
            return "减仓/回避"
        return "空仓观察"
