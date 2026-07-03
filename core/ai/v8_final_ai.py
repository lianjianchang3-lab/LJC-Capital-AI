from core.gateway import DataGateway, Signal


class V8FinalAI:
    def __init__(self, gateway=None):
        self.gateway = gateway or DataGateway()

    def _capital_score(self, cap):
        score = 55 + cap.main_inflow * 12 + cap.super_large * 8 + cap.large * 5
        return int(max(0, min(100, round(score))))

    def _risk_score(self, quote, cap):
        risk = 50
        if quote.change_pct > 6:
            risk += 20
        if quote.change_pct < -3:
            risk += 15
        if cap.main_inflow < 0:
            risk += 15
        return int(max(0, min(100, risk)))

    def _rank(self, lia):
        if lia >= 90:
            return "Diamond"
        if lia >= 80:
            return "Opportunity"
        if lia >= 68:
            return "Watch"
        return "Avoid"

    def _action(self, rank, risk):
        if rank == "Diamond" and risk < 65:
            return "持有 / 回调低吸"
        if rank == "Opportunity":
            return "小仓观察 / 等确认"
        if rank == "Watch":
            return "观察，不追高"
        return "暂不参与"

    def signals(self):
        quotes = {q.code: q for q in self.gateway.quotes()}
        capitals = {c.code: c for c in self.gateway.capital()}
        rows = []
        for code, q in quotes.items():
            c = capitals.get(code)
            if not c:
                continue
            capital_score = self._capital_score(c)
            risk = self._risk_score(q, c)
            trend = max(0, min(100, 65 + q.change_pct * 3))
            lia = round(capital_score * 0.45 + trend * 0.30 + (100 - risk) * 0.25, 1)
            rank = self._rank(lia)
            reason = f"行情来自{q.provider}，资金来自{c.provider}；主力净流入{c.main_inflow:.2f}，涨跌幅{q.change_pct:.2f}%"
            rows.append(Signal(code, q.name or c.name, q.price, q.change_pct, lia, capital_score, risk, rank, self._action(rank, risk), reason))
        return sorted(rows, key=lambda x: x.lia, reverse=True)

    def war_room(self):
        signals = self.signals()
        avg = sum(s.lia for s in signals) / len(signals) if signals else 0
        if avg >= 82:
            market = "Risk ON"
            position = "70%-85%"
        elif avg >= 70:
            market = "结构性机会"
            position = "50%-70%"
        else:
            market = "Risk OFF"
            position = "30%-50%"
        return {
            "market": market,
            "position": position,
            "top": signals[:10],
            "diamond": [s for s in signals if s.rank == "Diamond"],
            "opportunity": [s for s in signals if s.rank == "Opportunity"],
            "watch": [s for s in signals if s.rank == "Watch"],
        }
