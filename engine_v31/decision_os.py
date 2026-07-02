class V31DecisionOS:
    def __init__(self):
        self.watchlist = [
            ("300136", "信维通信", 95, 92, "Diamond Core", "持有/低吸做T"),
            ("300762", "上海瀚讯", 96, 94, "Diamond Core", "重点关注"),
            ("603308", "应流股份", 88, 82, "Opportunity", "观察资金持续性"),
            ("688008", "澜起科技", 91, 86, "Opportunity", "等待右侧确认"),
            ("688387", "信科移动", 86, 78, "Watch", "持续跟踪"),
        ]

    def run(self):
        diamond, opp, watch = [], [], []
        for code, name, lia, mfs, pool, action in self.watchlist:
            row = {
                "code": code,
                "name": name,
                "lia": lia,
                "mfs": mfs,
                "pool": pool,
                "action": action,
                "evidence": "主力资金纵向跟踪 + 研究评分 + 风险控制",
            }
            if pool == "Diamond Core":
                diamond.append(row)
            elif pool == "Opportunity":
                opp.append(row)
            else:
                watch.append(row)

        return {
            "war_room": {
                "market": "机构主线",
                "position": "75%",
                "theme": "商业航天 / AI基础设施",
                "risk": "LOW",
                "mission": "关注上海瀚讯，信维通信可低吸做T；不追高。",
            },
            "diamond": diamond,
            "opportunity": opp,
            "watch": watch,
            "capital": [
                "信维通信：近1日 +2.9亿，近3日 +7.6亿，趋势：连续增强",
                "上海瀚讯：近1日 +3.1亿，近3日 +8.1亿，趋势：连续增强",
                "应流股份：近1日 +0.3亿，近3日 +0.5亿，趋势：转弱观察",
            ],
        }
