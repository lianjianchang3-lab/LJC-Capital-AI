from core.v105.committee.committee_v5 import CommitteeV5

class PortfolioEngine105:
    def optimize(self):
        votes = CommitteeV5().decide().get("votes", [])
        buy = [x for x in votes if x["最终决策"] in ["重点买入关注","买入观察"]]
        watch = [x for x in votes if x["最终决策"] == "小仓观察"]
        cash = 1.0
        if len(buy) >= 3:
            cash = 0.35
        elif len(buy) >= 1:
            cash = 0.55
        elif len(watch) >= 3:
            cash = 0.70
        return {"status":"OK","cash_weight":cash,"buy_count":len(buy),"watch_count":len(watch),"summary":f"建议现金比例 {cash:.0%}，买入关注{len(buy)}只，小仓观察{len(watch)}只。"}
