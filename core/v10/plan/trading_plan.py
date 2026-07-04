from core.v10.committee import V10AICommittee

class V10TradingPlan:
    def generate(self):
        committee = V10AICommittee().decide()
        votes = committee.get("votes", [])
        plans = []
        for v in votes:
            price = float(v.get("现价", 0) or 0)
            if v.get("最终决策") == "买入关注":
                stop = round(price * 0.93, 2)
                t1 = round(price * 1.12, 2)
                t2 = round(price * 1.22, 2)
            elif v.get("最终决策") == "观察/小仓":
                stop = round(price * 0.94, 2)
                t1 = round(price * 1.08, 2)
                t2 = round(price * 1.15, 2)
            else:
                stop = None
                t1 = None
                t2 = None
            plans.append({
                "代码": v.get("代码"),
                "名称": v.get("名称"),
                "操作": v.get("最终决策"),
                "建议仓位": v.get("建议仓位"),
                "现价": price,
                "止损": stop,
                "目标一": t1,
                "目标二": t2,
                "投票数": v.get("投票数"),
                "理由": v.get("理由"),
            })
        return {
            "status": committee.get("status"),
            "summary": "自动交易计划已生成，仅作研究辅助，实盘需人工确认。",
            "plans": plans,
        }
