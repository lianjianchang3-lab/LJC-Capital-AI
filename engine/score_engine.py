class ScoreEngine:

    def __init__(self, cost):
        self.cost = cost

    def calculate(self):
        cost = self.cost

        score = 50

        # 机构成本结构
        if cost["机构成本结构"] == "强势多头":
            score += 20
        elif cost["机构成本结构"] == "偏强":
            score += 10

        # 机构浮盈
        if 0 <= cost["机构浮盈"] <= 15:
            score += 15
        elif 15 < cost["机构浮盈"] <= 25:
            score += 8
        elif cost["机构浮盈"] < 0:
            score -= 10

        # 获利盘比例
        if 40 <= cost["获利盘比例"] <= 85:
            score += 10
        elif cost["获利盘比例"] > 90:
            score -= 10

        # 派发风险
        if cost["派发风险"] == "低":
            score += 10
        elif cost["派发风险"] == "中":
            score += 3
        elif cost["派发风险"] == "高":
            score -= 15

        score = max(0, min(100, score))

        if score >= 90:
            level = "★★★★★ 强烈关注"
        elif score >= 80:
            level = "★★★★ 推荐关注"
        elif score >= 70:
            level = "★★★ 观察"
        else:
            level = "★★ 风险较高"

        return {
            "AI综合评分": score,
            "AI评级": level
        }