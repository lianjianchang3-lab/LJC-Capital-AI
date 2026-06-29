from models.stock_analysis import StockAnalysisResult


class DecisionEngine:

    def __init__(self, code, name, df):
        self.code = code
        self.name = name
        self.df = df.copy()

    def calculate(self):
        if self.df.empty or len(self.df) < 20:
            return StockAnalysisResult(
                code=self.code,
                name=self.name,
                recommendation="观察",
                evidence=["数据不足，无法形成有效判断"]
            )

        df = self.df
        latest = df.iloc[-1]
        close = latest["收盘"]

        ma5 = df["收盘"].tail(5).mean()
        ma10 = df["收盘"].tail(10).mean()
        ma20 = df["收盘"].tail(20).mean()

        score = 50
        evidence = []

        if close > ma5 > ma10 > ma20:
            score += 25
            bei = 85
            recommendation = "重点关注 / 可积极跟踪"
            evidence.append("收盘价站上MA5、MA10、MA20，趋势结构较强")
        elif close > ma20:
            score += 12
            bei = 70
            recommendation = "继续观察 / 条件合适可参与"
            evidence.append("股价站上20日均线，具备转强条件")
        else:
            score -= 10
            bei = 45
            recommendation = "暂不参与"
            evidence.append("股价未有效站上20日均线")

        volume_today = latest["成交量"]
        volume_avg5 = df["成交量"].tail(5).mean()

        if volume_today > volume_avg5 * 1.3:
            score += 15
            cri = 80
            evidence.append("成交量明显放大，资金活跃度提升")
        elif volume_today < volume_avg5 * 0.7:
            score -= 5
            cri = 45
            evidence.append("成交量偏弱，资金参与度不足")
        else:
            cri = 60
            evidence.append("成交量处于正常区间")

        high20 = df["最高"].tail(20).max()
        low20 = df["最低"].tail(20).min()

        if close >= high20 * 0.95:
            score += 10
            smi = 80
            evidence.append("股价接近20日高点，有突破动能")
        elif close <= low20 * 1.05:
            score -= 10
            smi = 40
            evidence.append("股价接近20日低点，短线风险偏高")
        else:
            smi = 60
            evidence.append("股价处于20日区间中部")

        score = max(0, min(100, round(score)))

        rri = max(0, min(100, 100 - abs(close - ma20) / ma20 * 100))
        ici = round((bei + cri + smi) / 3, 2)

        target_price = round(close * 1.12, 2)
        stop_loss = round(close * 0.92, 2)

        return StockAnalysisResult(
            code=self.code,
            name=self.name,
            ai_score=score,
            bei=bei,
            cri=cri,
            ici=ici,
            smi=smi,
            rri=round(rri, 2),
            recommendation=recommendation,
            target_price=target_price,
            stop_loss=stop_loss,
            evidence=evidence
        )