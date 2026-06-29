import pandas as pd


class CostEngine:

    def __init__(self, df):
        self.df = df.copy()

    def calculate(self):
        df = self.df
        result = {}

        latest = df.iloc[-1]["收盘"]
        high_60 = df["收盘"].tail(60).max()
        low_60 = df["收盘"].tail(60).min()

        result["最新价格"] = round(latest, 2)

        result["5日成本"] = round(df["收盘"].tail(5).mean(), 2)
        result["10日成本"] = round(df["收盘"].tail(10).mean(), 2)
        result["20日成本"] = round(df["收盘"].tail(20).mean(), 2)
        result["60日成本"] = round(df["收盘"].tail(60).mean(), 2)

        result["机构浮盈"] = round(
            (latest - result["20日成本"]) / result["20日成本"] * 100,
            2
        )

        result["60日高点"] = round(high_60, 2)
        result["60日低点"] = round(low_60, 2)

        result["获利盘比例"] = round(
            (latest - low_60) / (high_60 - low_60) * 100,
            2
        )

        result["套牢盘比例"] = round(100 - result["获利盘比例"], 2)

        if result["机构浮盈"] >= 25:
            result["派发风险"] = "高"
        elif result["机构浮盈"] >= 12:
            result["派发风险"] = "中"
        else:
            result["派发风险"] = "低"

        if latest > result["5日成本"] > result["10日成本"] > result["20日成本"]:
            result["机构成本结构"] = "强势多头"
        elif latest > result["20日成本"]:
            result["机构成本结构"] = "偏强"
        else:
            result["机构成本结构"] = "偏弱"

        if result["机构成本结构"] == "强势多头" and result["派发风险"] != "高":
            result["建仓/持仓判断"] = "机构持仓较健康"
        elif result["派发风险"] == "高":
            result["建仓/持仓判断"] = "注意高位派发风险"
        else:
            result["建仓/持仓判断"] = "需要继续观察"

        return result


