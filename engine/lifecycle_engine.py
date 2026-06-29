class LifecycleEngine:

    def __init__(self, cost):
        self.cost = cost

    def calculate(self):
        cost = self.cost

        score = cost["机构浮盈"]
        structure = cost["机构成本结构"]
        profit_ratio = cost["获利盘比例"]
        risk = cost["派发风险"]

        if structure == "偏弱" and score < 0:
            stage = "建仓/观察期"
            confidence = 70
        elif structure == "偏强" and 0 <= score <= 10:
            stage = "吸筹期"
            confidence = 78
        elif structure == "强势多头" and 0 <= score <= 15:
            stage = "启动期"
            confidence = 85
        elif structure == "强势多头" and 15 < score <= 25:
            stage = "主升浪"
            confidence = 88
        elif score > 25 and profit_ratio > 85:
            stage = "加速/派发警戒期"
            confidence = 82
        elif risk == "高":
            stage = "派发风险期"
            confidence = 80
        else:
            stage = "震荡观察期"
            confidence = 65

        return {
            "资金生命周期": stage,
            "生命周期可信度": confidence
        }