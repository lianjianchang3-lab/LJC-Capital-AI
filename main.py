import akshare as ak
from engine.cost_engine import CostEngine
from engine.score_engine import ScoreEngine
from engine.lifecycle_engine import LifecycleEngine

print("=" * 60)
print("        LJC Capital AI V6.4")
print("        资金生命周期版")
print("=" * 60)

code = input("请输入股票代码，例如 300136：")

df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")

if df.empty:
    print("读取失败：没有数据")
else:
    print()
    print("最近5日行情：")
    print(df.tail())

    cost_engine = CostEngine(df)
    cost = cost_engine.calculate()

    score_engine = ScoreEngine(cost)
    score = score_engine.calculate()

    lifecycle_engine = LifecycleEngine(cost)
    lifecycle = lifecycle_engine.calculate()

    print()
    print("=" * 60)
    print("机构成本引擎分析")
    print("=" * 60)

    print("最新价格：", cost["最新价格"])
    print("5日成本：", cost["5日成本"])
    print("10日成本：", cost["10日成本"])
    print("20日成本：", cost["20日成本"])
    print("60日成本：", cost["60日成本"])
    print("机构浮盈：", cost["机构浮盈"], "%")
    print("获利盘比例：", cost["获利盘比例"], "%")
    print("套牢盘比例：", cost["套牢盘比例"], "%")
    print("派发风险：", cost["派发风险"])
    print("机构成本结构：", cost["机构成本结构"])
    print("建仓/持仓判断：", cost["建仓/持仓判断"])

    print()
    print("=" * 60)
    print("资金生命周期")
    print("=" * 60)
    print("当前阶段：", lifecycle["资金生命周期"])
    print("可信度：", lifecycle["生命周期可信度"], "%")

    print()
    print("=" * 60)
    print("AI综合评分")
    print("=" * 60)
    print("AI评分：", score["AI综合评分"])
    print("AI评级：", score["AI评级"])

    print()
    print("分析完成！")