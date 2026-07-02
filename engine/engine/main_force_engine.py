class MainForceEngine:
    """
    主力资金纵向跟踪引擎。
    当前用模拟资金序列跑通逻辑；后续接真实资金流数据。
    """

    MOCK = {
        "300136": [1.2, 1.8, 2.6, 2.1, 2.9],
        "300762": [0.8, 1.4, 2.2, 2.8, 3.1],
        "603308": [0.5, 0.7, 0.4, -0.2, 0.3],
        "688008": [0.6, 0.9, 1.1, 1.4, 1.6],
        "688387": [0.2, 0.4, 0.7, 0.5, 0.8],
    }

    def evaluate(self, stock):
        series = self.MOCK.get(stock["code"], [0.1, 0.2, -0.1, 0.2, 0.1])
        mf_1d = round(series[-1], 2)
        mf_3d = round(sum(series[-3:]), 2)
        mf_5d = round(sum(series[-5:]), 2)
        acceleration = round(series[-1] - series[-2], 2)

        if all(x > 0 for x in series[-3:]) and acceleration > 0:
            trend = "连续增强"
            mfs = 92
        elif mf_3d > 0 and mf_5d > 0:
            trend = "持续流入"
            mfs = 84
        elif mf_3d < 0:
            trend = "转弱"
            mfs = 55
        else:
            trend = "震荡"
            mfs = 68

        return {
            "mf_1d": mf_1d,
            "mf_3d": mf_3d,
            "mf_5d": mf_5d,
            "mf_acc": acceleration,
            "main_force_trend": trend,
            "mfs": mfs,
        }
