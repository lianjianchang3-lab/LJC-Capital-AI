class MainForceTimelineEngine:
    def __init__(self):
        self.flow = {
            "300136": [0.8, 1.1, 1.4, 1.8, 2.1, 2.6, 2.9],
            "300762": [0.6, 1.0, 1.5, 2.2, 2.8, 3.0, 3.1],
            "603308": [0.9, 0.7, 0.5, 0.4, -0.2, 0.1, 0.3],
            "688008": [0.3, 0.5, 0.8, 0.9, 1.1, 1.4, 1.6],
            "688387": [0.2, 0.3, 0.4, 0.7, 0.5, 0.6, 0.8],
        }

    def analyze(self, code):
        series = self.flow.get(code, [0.1, 0.1, 0.0, 0.1, 0.2, 0.1, 0.2])
        one = round(series[-1], 2)
        three = round(sum(series[-3:]), 2)
        five = round(sum(series[-5:]), 2)
        accel = round(series[-1] - series[-2], 2)

        if all(x > 0 for x in series[-5:]) and accel > 0:
            state = "连续吸筹增强"
            score = 95
        elif all(x > 0 for x in series[-3:]):
            state = "持续流入"
            score = 86
        elif three < 0:
            state = "资金转弱"
            score = 55
        else:
            state = "震荡观察"
            score = 70

        return {
            "mf_1d": one,
            "mf_3d": three,
            "mf_5d": five,
            "mf_accel": accel,
            "capital_state": state,
            "capital_health": score,
            "timeline": series,
        }
