import pandas as pd


class ScannerEngine:
    def __init__(self, stock_list):
        self.stock_list = stock_list.copy()

    def calculate_score(self, row):
        score = 50

        try:
            pct = float(row["涨跌幅"])
            amount = float(row["成交额"])
            price = float(row["最新价"])
        except Exception:
            return 0

        # 涨幅评分
        if 3 <= pct <= 9:
            score += 20
        elif 0 < pct < 3:
            score += 10
        elif pct < 0:
            score -= 10

        # 成交额评分
        if amount >= 1_000_000_000:
            score += 20
        elif amount >= 500_000_000:
            score += 12
        elif amount >= 200_000_000:
            score += 6

        # 价格过滤
        if price < 2:
            score -= 20

        # 过度涨停附近降一点风险
        if pct > 9.5:
            score -= 5

        return max(0, min(100, round(score, 2)))

    def scan_top20(self):
        df = self.stock_list.copy()

        df["AI评分"] = df.apply(self.calculate_score, axis=1)

        df = df.sort_values(by="AI评分", ascending=False)

        return df[["代码", "名称", "最新价", "涨跌幅", "成交额", "AI评分"]].head(20)