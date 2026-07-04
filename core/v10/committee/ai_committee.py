import pandas as pd
from core.v10.market import V10MarketHub
from core.v10.fund import V10FundMonitor

class V10AICommittee:
    """
    AI投委会V4：资金、趋势、风险、量化、AI五票制。
    """
    def decide(self):
        df = V10MarketHub().quotes()
        if df.empty:
            return {"status": "NO DATA", "votes": [], "summary": "等待行情数据"}

        fund_items = pd.DataFrame(V10FundMonitor().analyze().get("items", []))
        fund_map = {}
        if not fund_items.empty and "code" in fund_items.columns and "主力强度" in fund_items.columns:
            fund_map = dict(zip(fund_items["code"], fund_items["主力强度"]))

        rows = []
        for _, r in df.iterrows():
            code = r.get("code")
            capital = float(r.get("capital", 0))
            trend = float(r.get("trend", 0))
            lia = float(r.get("lia", 0))
            risk = float(r.get("risk", 0))
            change = float(r.get("change_pct", 0))
            fund = float(fund_map.get(code, r.get("main_inflow", 0) * 35))

            votes = 0
            reasons = []
            if fund >= 70:
                votes += 1; reasons.append("资金强")
            if trend >= 70 or change >= 3:
                votes += 1; reasons.append("趋势强")
            if risk <= 55:
                votes += 1; reasons.append("风险可控")
            if capital >= 70:
                votes += 1; reasons.append("机构评分高")
            if lia >= 70:
                votes += 1; reasons.append("LIA强")

            if votes >= 4:
                decision = "买入关注"
                position = "8%-15%"
            elif votes >= 3:
                decision = "观察/小仓"
                position = "3%-8%"
            elif risk >= 75 or change <= -5:
                decision = "减仓/回避"
                position = "0%"
            else:
                decision = "观察"
                position = "0%-3%"

            rows.append({
                "代码": code,
                "名称": r.get("name"),
                "现价": r.get("price"),
                "涨跌幅": change,
                "投票数": votes,
                "最终决策": decision,
                "建议仓位": position,
                "主力强度": round(fund, 1),
                "风险": risk,
                "理由": "、".join(reasons) if reasons else "信号不足",
            })

        rows = sorted(rows, key=lambda x: (x["投票数"], x["主力强度"]), reverse=True)
        return {
            "status": "OK",
            "summary": f"AI投委会完成：{len(rows)}只，买入关注{sum(1 for x in rows if x['最终决策']=='买入关注')}只。",
            "votes": rows,
        }
