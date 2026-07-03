class AnalysisEngine:
    def main_force_summary(self, code, mf_df):
        rows = mf_df[mf_df["code"] == code].sort_values("date")
        if rows.empty:
            return {"mf_1d":0,"mf_3d":0,"mf_5d":0,"mf_10d":0,"capital_health":50,"capital_state":"暂无资金数据","latest_date":"-"}
        s = rows["main_force"].tolist()
        one = round(s[-1],2)
        three = round(sum(s[-3:]),2)
        five = round(sum(s[-5:]),2)
        ten = round(sum(s[-10:]),2)
        accel = round(s[-1]-s[-2],2) if len(s)>=2 else 0
        if len(s)>=5 and all(x>0 for x in s[-5:]) and accel>0:
            state, score = "连续吸筹增强", 95
        elif len(s)>=3 and all(x>0 for x in s[-3:]):
            state, score = "持续流入", 86
        elif three < 0:
            state, score = "资金转弱", 55
        else:
            state, score = "震荡观察", 70
        return {"mf_1d":one,"mf_3d":three,"mf_5d":five,"mf_10d":ten,"mf_accel":accel,
                "capital_health":score,"capital_state":state,"latest_date":str(rows.iloc[-1]["date"].date())}

    def pool_decision(self, base, risk, mf):
        lia = round(base*0.55 + mf["capital_health"]*0.35 + (100-risk)*0.10, 1)
        confidence = round(min(98, lia - risk*0.05), 1)
        if lia >= 90 and mf["capital_health"] >= 88 and risk <= 25:
            return lia, confidence, "Diamond Core", "持有/低吸做T", "S"
        if lia >= 84 and mf["capital_health"] >= 78:
            return lia, confidence, "Opportunity", "等待右侧确认", "A"
        return lia, confidence, "Watch", "持续跟踪", "B"
