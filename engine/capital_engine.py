class CapitalEngine:

    def __init__(self, cost):
        self.cost = cost

    def calculate(self):

        profit = self.cost["获利盘比例"]
        floating = self.cost["机构浮盈"]

        # 主力控盘度（经验模型）
        control = round(
            min(
                max(
                    profit * 0.55 + floating * 1.2,
                    5
                ),
                95
            ),
            1
        )

        # 散户比例
        retail = round(100 - control, 1)

        # 资金画像
        if control >= 80:
            fund_type = "机构高度控盘"
            institution = "★★★★★"
        elif control >= 65:
            fund_type = "机构主导"
            institution = "★★★★☆"
        elif control >= 50:
            fund_type = "机构+游资"
            institution = "★★★☆☆"
        elif control >= 35:
            fund_type = "游资活跃"
            institution = "★★☆☆☆"
        else:
            fund_type = "散户行情"
            institution = "★☆☆☆☆"

        return {

            "机构评分": institution,

            "主力控盘": control,

            "散户比例": retail,

            "资金画像": fund_type

        }